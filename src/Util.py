from pathlib import Path
from Exceptions import LinkException


def link(slayer: Path, olayer: Path, path: Path):
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
	# ERROR
	raise LinkException(f"Could not link {olayer/path} and {olayer/path}")
	

	