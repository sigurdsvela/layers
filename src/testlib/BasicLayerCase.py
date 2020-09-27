from unittest import TestCase
from pathlib import Path
import os
import copy
import subprocess
from layers.cli import Runner, commands
from layers.lib import GlobalConsts,LayerLocalPath,Layer,LayerSet

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
        path.mkdir(parents=True)
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
        layers:[Path] = [TEST_ENV / layerPath for layerPath in TEST_STRUCT['layers']]

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
        for layerPath in layers:
            Runner().quiet().run(command=commands.New, level=-1, target_layer=layers[0], mount=layerPath)


    def tearDown(self):
        os.chdir(self._prev_cwd)
        subprocess.Popen(["rm", "-rf", TEST_ENV]).wait()

    def verify(self) -> [Exception]:
        errors = []
        # Verify that all files are linked to all layers
        for f in self.files:
            for layer in f.layer.layers:
                if layer.path != f.layer.path:
                    if not f.inLayer(layer).path.resolve().absolute().exists():
                        errors.append(FileNotFoundError(f"Layer {layer.level}@{layer.path} missing link to {f.localPath} in layer {f.layer.level}@{f.layer.path}"))
                    if f.inLayer(layer).path.resolve().absolute() != f.path.resolve().absolute():
                        errors.append(FileNotFoundError(f"Layer {layer.level}@{layer.path} and {f.layer.level}@{f.layer.path} has conflicting content for file {f.localPath}"))

        # Verify that all links point to the same, and a valid and present file
        for l in self.links:
            if not l.path.resolve(strict=False).exists():
                errors.append(FileNotFoundError(f"Broken link in layer {l.layer.level}@{l.layer.path} file {l.localPath} -> {l.path.resolve(strict=False)}"))

        # Verify all .layers config files
        baseConfig = LayerSet.fromLayer(self.layers[0]).baseLayer.config.path

        for layer in self.layers:
            if not baseConfig == layer.config.path.resolve():
                errors.append(FileNotFoundError(f"Layer {layer.level}@{layer.path} config file does not link to baselayer."))

        return errors

    def assertVerify(self):
        self.assertFalse(self.verify())

    def sync(self):
        Runner().quiet().run(command=commands.Sync, target_layer=self.layers[0].path)
        return self.verify()

    def fsStruct(self, path=TEST_ENV, root=TEST_ENV):
        struct = {'type':'dir', 'path':path, 'content': {}}

        files = os.listdir(path)

        for f in files:
            fp = path/f

            if fp.is_symlink():
                struct['content'][f] = {
                    'type': 'link',
                    'dst_type': 'dir' if fp.resolve().absolute().is_dir() else 'file',
                    'path': fp.relative_to(root),
                    'content': fp.resolve().absolute().relative_to(root)
                }

            elif fp.is_file():
                struct['content'][f] = {
                    'type': 'file',
                    'path': fp.relative_to(root),
                    'content': (fh := fp.open('r')).read()
                }
                fh.close()

            elif fp.is_dir():
                struct['content'][f] = self.fsStruct(path/fp)

        return struct
                
    def printStruct(self, struct, indent=1, indentStr="|  "):
        Black = "\u001b[30m"
        Red = "\u001b[31m"
        Green = "\u001b[32m"
        Yellow = "\u001b[33m"
        Blue = "\u001b[34m"
        Magenta = "\u001b[35m"
        Cyan = "\u001b[36m"
        White = "\u001b[37m"
        Grey = "\u001b[37m"
        Reset = "\u001b[0m"

        _indentStr = indentStr.join(["" for n in range(0, indent)])

        for name in struct['content']:
            print(Reset, end="")
            print(_indentStr, end="")

            f = struct['content'][name]
            if f['type'] == 'dir':
                print(Blue, end="")
                print(f"{name}/")
                self.printStruct(f, indent+1)
                continue
            
            if f['type'] == 'file':
                contentPrefix = f"{_indentStr}      |-  "
                content = f"\n{contentPrefix}".join(f['content'].split('\n'))
                print(White, end="")
                print(name)
                # print(contentPrefix + content)
                # print(Reset, end="")
            
            if f['type'] == 'link':
                print(Cyan, end="")
                if f['dst_type'] == 'dir':
                    print(f"{name}/ -> {f['content']}/")
                else:
                    print(f"{name} -> {f['content']}")

        print(Reset, end="")

    def printFsStruct(self):
        print()
        self.printStruct(self.fsStruct())

   
    @property
    def files(self) -> [LayerLocalPath]:
        files:[LayerLocalPath] = []
        for layer in TEST_STRUCT['layers']:
            layerPath = (TEST_ENV / layer).absolute()
            for root, dirs, _files in os.walk(layerPath):
                for f in _files:
                    p = Path(root)/f
                    if p.is_file() and not p.is_symlink():
                        files.append(LayerLocalPath(layer=layerPath, path=p.relative_to(layerPath)))
        return [f for f in files if str(f.localPath) != GlobalConsts.LAYER_CONFIG_FILE]

    @property
    def links(self) -> [LayerLocalPath]:
        files:[LayerLocalPath] = []
        for layer in TEST_STRUCT['layers']:
            layerPath = (TEST_ENV / layer).absolute()
            for root, dirs, _files in os.walk(layerPath):
                for f in _files:
                    p = Path(root)/f
                    if p.is_symlink():
                        files.append(LayerLocalPath(layer=layerPath, path=p.relative_to(layerPath)))
        return [f for f in files if str(f.localPath) != GlobalConsts.LAYER_CONFIG_FILE]


    def filesIn(self, level:int) -> [LayerLocalPath]:
        files:[LayerLocalPath] = []
        layerPath = (TEST_ENV / str(self.layers[level])).absolute()
        for root, dirs, _files in os.walk(layerPath):
            for f in _files:
                p = Path(root)/f
                if p.is_file() and not p.is_symlink():
                    files.append(LayerLocalPath(layer=layerPath, path=p.relative_to(layerPath)))
        return [f for f in files if str(f.localPath) != GlobalConsts.LAYER_CONFIG_FILE]

    def findFile(self, filt: callable(LayerLocalPath)):
        for f in self.files:
            if filt(f):
                return f
        return None

    @property
    def layers(self):
        return [Layer(TEST_ENV / layerPath) for layerPath in TEST_STRUCT['layers']]

    @property
    def root(self):
        return TEST_ENV

    