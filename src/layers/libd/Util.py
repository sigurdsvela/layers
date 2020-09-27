from pathlib import Path
import os
TEST_ENV = Path("/home/docker/layers/tests/test-dir/")
class Util:
    @classmethod
    def linkFrom(cls, frm: Path, to: Path, path: Path):
        if not (to/path).exists():
            FileNotFoundError()

        if not (frm/path).exists():
            (frm/path).symlink_to((to/path).resolve().absolute())
            return

        if (to/path).resolve().absolute() == (frm/path).resolve().absolute():
            return 

        # We will link each file inside the directory instead
        if (frm/path).is_dir() and (to/path).is_dir():
            return

        raise FileExistsError()
        
    @classmethod
    def bilink(cls, slayer: Path, olayer: Path, path: Path):
        if not (slayer/path).exists():
            if not (olayer/path).exists():
                raise FileNotFoundError(f"{str(slayer/path)}, {str(olayer/path)}")
            else:
                # Linking form olayer to slayer
                (slayer/path).symlink_to(olayer/path)
                return

        if not (olayer/path).exists():
            if not (slayer/path).exists():
                raise FileNotFoundError(f"{str(slayer/path)}, {str(olayer/path)}")
            else:
                # Linking from slayer to olayer
                (olayer/path).symlink_to(slayer/path)
                return

        if (olayer/path).resolve() == (slayer/path).resolve():
            return # They already point to the same file


        # Not neccesarily a conflict if they are directories.
        # This is assumed linked, moving on
        if (olayer/path).is_dir() and (slayer/path).is_dir():
            return

        # Both exist
        # But the do not point to the same file
        # And they are not directories.
        raise FileExistsError(f"Could not link {olayer/path} and {olayer/path}")
