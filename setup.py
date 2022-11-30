import py2exe
if __name__ == "__main__":
    py2exe.freeze(
        console=['main.py'],
        windows=[],
        data_files=None,
        zipfile=None,
        options={
            'bundle_files':1,
            'compressed': True},
        version_info={
            "version":"1.0",
        }
    )