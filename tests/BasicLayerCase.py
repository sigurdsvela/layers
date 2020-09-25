from LayerLocalPath import LayerLocalPath
import GlobalConsts
from unittest import TestCase
from pathlib import Path
import os
import subprocess

TEST_ENV = Path('./tests/test-dir').resolve().absolute()
TEST_STRUCT = {
    "layers": ["layer1", "dir1/subdir1/layer2", "dir1/subdir2/layer3"],

    "paths": {
        "layer1": {
            "rootfile_layer1" : "C9E56E0B-A053-4B8F-886E-6A9F80E1F1F5"
        },
        "dir1": {
            "subdir1": {
                "layer2": {
                    "rootfile_layer2": "C506CE86-9A6A-49FA-B60A-8AFCA9544126",
                    "shared_sublayer_2_3_dir": {
                        "shared_sublayer_2_3_dir_layer2_file1": "DBFC281D-279F-4149-93F5-ADE24D9CD597",
                        "shared_sublayer_2_3_dir_layer2_file2": "4A0905CA-F0D6-4779-8D7B-B76497173090",
                        "shared_sublayer_2_3_dir_subdir" : {
                            "shared_sublayer_2_3_dir_subdir_layer2_file2": "B8D401C9-5B46-4F6E-A7F0-6AC94DF1E235" 
                        }
                    }
                }
            },
            "subdir2": {
                "layer3": {
                    "rootfile_layer3" : "248DC900-381A-4895-939D-CC18FB4B37DC",
                    "shared_sublayer_2_3_dir": {
                        "shared_sublayer_2_3_dir_layer3_file1": "FF934BB1-DE6F-4940-B122-0F5CF44EA1CA"
                    },
                    "layer3_subdir": {
                        "file1": "3F8999E4-099E-4AFE-A8D9-0E22224F730F",
                        "file2": "5E12432A-EC4D-40FD-A7F8-9B21F60BAE31",
                        "file3": "85C21E27-3432-4261-B2DB-6276A16A67D4",
                        "file4": "E8CF5D8D-F3AD-4FD2-A9EE-F4ABF6DCB729"
                    }
                }
            }
        },
    }
}


class BasicLayerCase(TestCase):
    def _mkfs(self, path: Path, obj: dict):
        path.mkdir()
        for name in obj:
            if type(obj[name]) is str:
                (path / name).touch()
                (fh := (path / name).open('w')).write(obj[name])
                fh.close()
            elif type(obj[name]) is dict:
                self._mkfs(path/name, obj[name])
            else:
                TypeError(f"Expecting all entries in directory structur to be of either `dict` or `str`. Got {type(obj[name]):s}")

    def setUp(self):
        self._layers:[Path] = [TEST_ENV / layerPath for layerPath in TEST_STRUCT['layers']]

        # Create testenv dir, and go in
        try:
            self._prev_cwd = Path(os.getcwd()).absolute()
        except:
            self._prev_cwd = Path("/")

        if TEST_ENV.exists():
            subprocess.Popen(["rm", "-rf", TEST_ENV]).wait()

        # Make filestructur
        self._mkfs(TEST_ENV, TEST_STRUCT['paths'])
        # Chdir to root of new fs
        os.chdir(TEST_ENV)
        # Make the layers
        for layerPath in self.layers:
            subprocess.Popen(["layers", "-v", "-l", self.layers[0], "new", layerPath]).wait()


    def tearDown(self):
        os.chdir(self._prev_cwd)
        subprocess.Popen(["rm", "-rf", TEST_ENV]).wait()

    def verify(self):
        errors = []

        layers = self.layers

        for root, dirs, files in os.walk(self.root/layers[0]):
            paths = dirs
            paths.extend(files)
            paths = [Path(p) for p in paths]
            for path in paths:
                lPath = (root/path).relative_to(self.root/layers[0])

                # If link, check that link resolves
                if (layers[0]/lPath).is_symlink():
                    if not (layers[0]/lPath).resolve(strict=False).exists():
                        errors.append(FileNotFoundError(f"Broken link '{(layers[0]/lPath)}' -> '{(layers[0]/lPath).resolve(strict=False)}'"))
                else: # Check that all other layers also link to this file
                    for layer in layers[1:]:
                        if not (layer/lPath).exists():
                            errors.append(FileNotFoundError(f"Layer at '{layer}' missing link at '{(layer/lPath)}' to file '{(layers[0]/lPath).resolve().absolute()}'"))
                        elif not (layer/lPath).is_symlink():
                            errors.append(FileExistsError(f"Conflicting file {lPath}. Exists in layer '{layers[0]}' and '{layer}'"))
                        elif not (layer/lPath).resolve(strict=False).absolute().exists():
                            errors.append(FileNotFoundError(f"Broken link '{(layer/lPath)}' -> '{(layer/lPath).resolve(strict=False)}'"))
                        elif not (layer/lPath).resolve() == (layers[0]/lPath).resolve():
                            errors.append(FileNotFoundError(f"Conflicting link in layers '{layer}' and '{layers[0]}': '{(layer/lPath).resolve().absolute()}'<-'{lPath}'->'{(layers[0]/lPath).resolve().absolute()}'."))
        
        return errors


    def sync(self):
        subprocess.Popen(["layers", "-v", "-l", self.layers[0], "sync"]).wait()
        return self.verify()

    def files(self) -> LayerLocalPath:
        files:[LayerLocalPath] = []
        for layer in TEST_STRUCT['layers']:
            layerPath = (TEST_ENV / layer).absolute()
            for root, dirs, _files in os.walk(layerPath):
                for f in _files:
                    p = Path(root)/f
                    if p.is_file() and not p.is_symlink():
                        files.append(LayerLocalPath(layer=layerPath, path=p.relative_to(layerPath)))
        return [f for f in files if str(f.path) != GlobalConsts.LAYER_CONFIG_FILE]


    @property
    def layers(self):
        return self._layers

    @property
    def root(self):
        return TEST_ENV

    