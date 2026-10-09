"""Tests for the pure (non-GUI) functions in file_janitor.py."""

import hashlib
import os

import file_janitor


def _write(path, content, mtime):
    path.write_bytes(content)
    os.utime(path, (mtime, mtime))


# --- hash_file ---

def test_hash_file_known_content(tmp_path):
    target = tmp_path / "hello.txt"
    target.write_bytes(b"hello world")
    expected = hashlib.sha256(b"hello world").hexdigest()
    assert file_janitor.hash_file(str(target)) == expected


def test_hash_file_missing_returns_none(tmp_path):
    assert file_janitor.hash_file(str(tmp_path / "does-not-exist.txt")) is None


# --- find_duplicates ---

def test_find_duplicates_groups_identical_content(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"same bytes")
    (tmp_path / "b.txt").write_bytes(b"same bytes")
    (tmp_path / "unique.txt").write_bytes(b"something else")

    duplicates = file_janitor.find_duplicates(str(tmp_path))

    assert len(duplicates) == 1
    paths = next(iter(duplicates.values()))
    assert sorted(os.path.basename(p) for p in paths) == ["a.txt", "b.txt"]


def test_find_duplicates_empty_when_all_unique(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"one")
    (tmp_path / "b.txt").write_bytes(b"two")
    assert file_janitor.find_duplicates(str(tmp_path)) == {}


# --- find_empty_folders ---

def test_find_empty_folders_finds_nested_empties(tmp_path):
    (tmp_path / "empty1").mkdir()
    (tmp_path / "empty2" / "nested").mkdir(parents=True)
    nonempty = tmp_path / "nonempty"
    nonempty.mkdir()
    (nonempty / "file.txt").write_text("x")

    empties = file_janitor.find_empty_folders(str(tmp_path))
    names = {os.path.basename(p) for p in empties}

    assert {"empty1", "empty2", "nested"} <= names
    assert "nonempty" not in names


# --- handle_duplicates ---

def _duplicate_setup(tmp_path):
    content = b"duplicate content"
    old = tmp_path / "old.txt"
    new = tmp_path / "new.txt"
    backup_dir = tmp_path / "mybackup"
    backup_dir.mkdir()
    protected = backup_dir / "copy.txt"
    _write(old, content, 1_000)
    _write(new, content, 2_000)
    _write(protected, content, 500)
    digest = hashlib.sha256(content).hexdigest()
    return digest, old, new, protected


def test_handle_duplicates_yes_deletes_older_keeps_newest_and_backup(tmp_path, monkeypatch):
    digest, old, new, protected = _duplicate_setup(tmp_path)
    report = []
    monkeypatch.setattr("builtins.input", lambda _: "y")

    file_janitor.handle_duplicates({digest: [str(old), str(new), str(protected)]}, report)

    assert os.path.exists(str(new)), "newest copy must be kept"
    assert not os.path.exists(str(old)), "older copy must be deleted"
    assert os.path.exists(str(protected)), "file inside a backup path must be protected"
    assert any("PROTECTED" in line and "copy.txt" in line for line in report)
    assert any("DELETED" in line and "old.txt" in line for line in report)


def test_handle_duplicates_no_skips_deletion(tmp_path, monkeypatch):
    digest, old, new, _protected = _duplicate_setup(tmp_path)
    report = []
    monkeypatch.setattr("builtins.input", lambda _: "n")

    file_janitor.handle_duplicates({digest: [str(old), str(new)]}, report)

    assert os.path.exists(str(old))
    assert os.path.exists(str(new))
    assert any("skipped" in line.lower() for line in report)


def test_handle_duplicates_nothing_to_do(tmp_path):
    report = []
    file_janitor.handle_duplicates({}, report)
    assert any("No duplicate files found" in line for line in report)
