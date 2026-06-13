"""
Agent Evaluator - py2app 打包脚本

使用方法:
    pip install py2app
    python packaging/py2app_setup.py py2app

产出: dist/Agent评估框架.app
"""

from setuptools import setup

APP = ["src/macos/app.py"]
DATA_FILES = [
    ("src/web/static", ["src/web/static/index.html"]),
]

OPTIONS = {
    "argv_emulation": False,
    "plist": {
        "CFBundleName": "Agent评估框架",
        "CFBundleDisplayName": "Agent 评估框架",
        "CFBundleIdentifier": "com.dirjaker.agent-evaluator",
        "CFBundleVersion": "1.0.0",
        "CFBundleShortVersionString": "1.0.0",
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "10.15",
    },
    "packages": [
        "fastapi",
        "uvicorn",
        "pydantic",
        "starlette",
    ],
    "includes": [
        "src",
        "src.evaluator",
        "src.test_dataset",
        "src.benchmark",
        "src.web",
        "src.web.app",
        "src.macos",
    ],
    "excludes": [
        "matplotlib",
        "numpy",
        "pandas",
        "scipy",
        "PIL",
    ],
}

setup(
    name="Agent评估框架",
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
