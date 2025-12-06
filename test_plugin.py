"""
Simple test script to validate the plugin's core functionality
"""
import sys
from pathlib import Path

# Add parent directory to path to import the plugin
sys.path.insert(0, str(Path(__file__).parent))

from nonebot_plugin_mhy_choose import get_image_files, IMAGE_EXTENSIONS


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


if __name__ == "__main__":
    print("Running tests for nonebot_plugin_mhy_choose...\n")
    print("=" * 50)
    
    try:
        test_image_extensions()
        test_get_image_files_empty_folder()
        test_get_image_files_with_images()
        test_get_image_files_subdirectories()
        test_get_image_files_nonexistent_folder()
        
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
