#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

# README 파일 읽기
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# requirements.txt 읽기
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="starwargez-comment-collector",  # PyPI에서 고유한 패키지명
    version="1.1.0",
    author="pepe-made-it",
    author_email="for.miracle.course@gmail.com",  # 실제 이메일로 변경
    description="빛이왔다 스타워게즈 댓글 자동 수집기",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pepe-made-it/cafe_count",
    packages=find_packages(),
    py_modules=["main", "gui_main"],  # 단일 모듈들
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: Korean",
    ],
    license="MIT",
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "starwargez-gui=gui_main:main",  # GUI 버전 명령어
            "starwargez-cli=main:main",     # CLI 버전 명령어
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.bat", "*.sh"],
    },
    keywords="naver cafe comment scraper selenium automation korean",
    project_urls={
        "Bug Reports": "https://github.com/pepe-made-it/cafe_count/issues",
        "Source": "https://github.com/pepe-made-it/cafe_count/",
        "Documentation": "https://github.com/pepe-made-it/cafe_count/blob/main/README.md",
    },
) 