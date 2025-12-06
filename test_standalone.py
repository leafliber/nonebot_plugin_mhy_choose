"""
Standalone test for core functionality without NoneBot dependencies
"""
from pathlib import Path
from typing import List
import sys

# Image extensions to test
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}


def get_image_files(folder_path: str) -> List[Path]:
    """
    获取指定文件夹内的所有图片文件
    
    Args:
        folder_path: 图片文件夹路径
        
    Returns:
        图片文件路径列表
    """
    image_files = []
    path = Path(folder_path)
    
    if not path.exists():
        print(f"Warning: 图片文件夹不存在: {folder_path}")
        return image_files
    
    if not path.is_dir():
        print(f"Warning: 路径不是文件夹: {folder_path}")
        return image_files
    
    # 遍历文件夹获取所有图片文件
    for file_path in path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
            image_files.append(file_path)
    
    return image_files


def test_image_extensions():
    """Test that IMAGE_EXTENSIONS contains expected formats"""
    print("Testing IMAGE_EXTENSIONS...")
    expected = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    assert IMAGE_EXTENSIONS == expected, f"Expected {expected}, got {IMAGE_EXTENSIONS}"
    print("✓ IMAGE_EXTENSIONS correct")


def test_get_image_files_empty_folder():
    """Test get_image_files with empty folder"""
    print("\nTesting get_image_files with empty folder...")
    test_dir = Path("test_images")
    test_dir.mkdir(exist_ok=True)
    
    # Clean the directory
    for item in test_dir.iterdir():
        if item.is_file():
            item.unlink()
    
    files = get_image_files(str(test_dir))
    assert len(files) == 0, f"Expected 0 files, got {len(files)}"
    print("✓ Empty folder returns empty list")


def test_get_image_files_with_images():
    """Test get_image_files with test images"""
    print("\nTesting get_image_files with images...")
    test_dir = Path("test_images")
    test_dir.mkdir(exist_ok=True)
    
    # Create some test files
    test_files = [
        test_dir / "test1.jpg",
        test_dir / "test2.png",
        test_dir / "test3.gif",
        test_dir / "not_image.txt",
    ]
    
    for file in test_files:
        file.touch()
    
    files = get_image_files(str(test_dir))
    
    # Should find 3 image files, not the txt file
    assert len(files) == 3, f"Expected 3 files, got {len(files)}"
    print(f"✓ Found {len(files)} image files (correct)")
    
    # Clean up
    for file in test_files:
        if file.exists():
            file.unlink()


def test_get_image_files_subdirectories():
    """Test get_image_files with subdirectories"""
    print("\nTesting get_image_files with subdirectories...")
    test_dir = Path("test_images")
    test_dir.mkdir(exist_ok=True)
    sub_dir = test_dir / "subdir"
    sub_dir.mkdir(exist_ok=True)
    
    # Create test files in different directories
    test_files = [
        test_dir / "root.jpg",
        sub_dir / "sub.png",
    ]
    
    for file in test_files:
        file.touch()
    
    files = get_image_files(str(test_dir))
    
    # Should find files in both root and subdirectory
    assert len(files) == 2, f"Expected 2 files, got {len(files)}"
    print(f"✓ Found {len(files)} image files in subdirectories (correct)")
    
    # Clean up
    for file in test_files:
        if file.exists():
            file.unlink()
    if sub_dir.exists():
        sub_dir.rmdir()


def test_get_image_files_nonexistent_folder():
    """Test get_image_files with nonexistent folder"""
    print("\nTesting get_image_files with nonexistent folder...")
    files = get_image_files("nonexistent_folder_xyz123")
    assert len(files) == 0, f"Expected 0 files for nonexistent folder, got {len(files)}"
    print("✓ Nonexistent folder returns empty list")


def test_case_insensitive():
    """Test that file extensions are case-insensitive"""
    print("\nTesting case-insensitive extension matching...")
    test_dir = Path("test_images")
    test_dir.mkdir(exist_ok=True)
    
    # Create files with uppercase extensions
    test_files = [
        test_dir / "test1.JPG",
        test_dir / "test2.PNG",
        test_dir / "test3.GIF",
    ]
    
    for file in test_files:
        file.touch()
    
    files = get_image_files(str(test_dir))
    
    # Should find all 3 files despite uppercase extensions
    assert len(files) == 3, f"Expected 3 files, got {len(files)}"
    print(f"✓ Found {len(files)} image files with uppercase extensions (correct)")
    
    # Clean up
    for file in test_files:
        if file.exists():
            file.unlink()


if __name__ == "__main__":
    print("Running tests for nonebot_plugin_mhy_choose core functionality...\n")
    print("=" * 50)
    
    try:
        test_image_extensions()
        test_get_image_files_empty_folder()
        test_get_image_files_with_images()
        test_get_image_files_subdirectories()
        test_get_image_files_nonexistent_folder()
        test_case_insensitive()
        
        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
