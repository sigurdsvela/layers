from pathlib import Path

def confirmLinkedSet(*paths: [Path]):
	original = None

	for p in paths:
		if not p.is_symlink():
			if not original == None: # Multiple not symlinked files
				return False
			else:
				original = p

	if original == None:
		return False # Could not find original

	for p in paths:
		if not p.resolve().absolute() == original.resolve().absolute():
			return False # At least one file was not linked to the same place

	return True