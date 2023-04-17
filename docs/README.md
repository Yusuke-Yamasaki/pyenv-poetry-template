# Python環境構築

基本的に仮想環境を構築してPythonを運用する際の手引きをまとめてます．

# How to install python modules

参考：[Python Environment variables (Official Documents)](https://docs.python.org/3.8/using/cmdline.html#environment-variables)

> On Linux systems, a Python installation will typically be included as part of the distribution. Installing into this Python installation requires root access to the system, and may interfere with the operation of the system package manager and other components of the system if a component is unexpectedly upgraded using `pip`.
> 
> 
> On such systems, it is often better to use a virtual environment or a per-user installation when installing packages with `pip`.
> 参考：[Installing Python Modules (Official Documents)](https://docs.python.org/3.8/installing/index.html)
> 

ということで仮想環境を使ったパッケージ管理が推奨されている．
仮想環境の導入によりisolated Python interpreterをプロジェクトごとに切り替えることができる．UNIXのデフォルトのPython interpreterは`/usr/local/bin/python`であり，shellの検索パスに`/usr/local/bin`を追加することで呼び出せる．自身で新たに入れたPython interpreterを使用するには，デフォルトより優先されるように検索パスを設定する必要がある．(検索パスは前から読むので)

> When you run Python, the module search path `sys.path` usually includes a directory whose path ends in `"site-packages"`. This directory is intended to hold locally-installed packages available to all users using a machine or a particular site installation.
引用：[PEP 370: Per-user site-packages Directory](https://docs.python.org/3.8/whatsnew/2.6.html#pep-370-per-user-site-packages-directory)
> 

さらに，仮想環境ごとにisolated site directory `*/python3.x/lib/site-packages`をもつので，他の環境に影響を与えることなくパッケージ管理もできる．仮想環境についての詳細は[PEP405](https://peps.python.org/pep-0405/)に記載．

> As initialized upon program startup, the first item of this list, `path[0]`, is the directory containing the script that was used to invoke the Python interpreter. If the script directory is　not available (e.g. if the interpreter is invoked interactively or if the script is read from standard input), `path[0]` is the empty string, which directs Python to search modules in the current directory first. Notice that the script directory is inserted before the entries inserted as a result of `$PYTHONPATH`.
引用：[sys.path](https://docs.python.org/3.8/library/sys.html#sys.path)
> 

モジュールの検索パスの優先度はPython interpreterを起動したディレクトリ＞`$PYTHONPATH`内で規定する順となる．

# バージョン管理ツール

## pyenv

参考：[公式リポジトリ](https://github.com/pyenv/pyenv)

pythonのバージョンを使い分けるためのツールで作業ディレクトリごとにpythonのバージョンを設定可能．

### How it works

rbenvからforkされており，どちらも”shim design philosophy”を採用している．まず，$PATHの先頭にshimsのディレクトリを追加する．

```bash
$(pyenv root)/shims:/usr/local/bin:/usr/bin:/bin
```

すると，検索パス上では`/usr/local/bin/python`の前に`$(pyenv root)/shims/python`が見つかる．これをinterceptと呼んでいて，shimコマンドがinterceptして所望のバージョンを利用するという流れになっている．具体的には，`$(pyenv root)/shims/`配下のコマンドをshimコマンドと呼ぶが，shimコマンドの実行時に，pyenvがPythonのどのバージョンを使うかを決定する．バージョンの優先順位は以下の通り

1. $PYENV_VERSION
2. 現ディレクトリにある`.python-version`ファイル
3. 現ディレクトリの上位階層で初めて見つかった`.python-version`ファイル
4. `$(pyenv root)/version`ファイル

`pyenv which <command>` により，shim経由で<command>を実行した際に，実際に走る実行ファイルを確認できる．

```bash
pyenv which python2.5
>> $(pyenv root)/versions/2.5.2/bin/python2.5
```

### Installation

[Suggested Build Environment](https://github.com/pyenv/pyenv/wiki#troubleshooting--faq)

```bash
sudo apt update; sudo apt install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

```bash
yum install gcc make zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel
```

**Check out Pyenv where you want it installed.** A good place to choose is `$HOME/.pyenv` (but you can install it somewhere else):

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

### Setup your shell environment for Pyenv

- Define environment variable `PYENV_ROOT` to point to the path where Pyenv will store its data. `$HOME/.pyenv` is the default. If you installed Pyenv via Git checkout, we recommend to set it to the same location as where you cloned it.
- Add the `pyenv` executable to your `PATH` if it's not already there
- run `eval "$(pyenv init -)"` to install `pyenv` into your shell as a shell function, enable shims and autocompletion
    - You may run `eval "$(pyenv init --path)"` instead to just enable shims, without shell integration

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

### How to use

必要なバージョン<version>(ex: 3.8.0, etc…)を指定してインストールするとソースのダウンロードおよびビルドをしてくれる．

```bash
pyenv install <version>
```

pyenvでインストールしたバージョンの切り替え方

- `pyenv local <version>` — automatically select whenever you are in the current directory or its subdirectories
    - 実行したディレクトリに.pyenv-versionが作成される．下層から探索するので，実行したディレクトリ以下ではglobalよりもlocalで指定したものが優先される．
- `pyenv global <version>` — select globally for your user account
    - `$PYENV_ROOT/version`に記載される．

# パッケージ管理ツール

参考：[Pythonパッケージングの標準を知ろう（Recruit Tech Blog）](https://engineer.recruit-lifestyle.co.jp/techblog/2019-12-25-python-packaging-specs/)

参考：[pipとpipenvとpoetryの技術的・歴史的背景とその展望（ばんくしさんのBlog）](https://vaaaaaanquish.hatenablog.com/entry/2021/03/29/221715)

参考：[Pythonのパッケージ周りのベストプラクティスを理解する（M3 Tech Blog）](https://www.m3tech.blog/entry/python-packaging)

## pip

参考：[User Guide (Official Documents)](https://pip.pypa.io/en/stable/user_guide/)

### How it works

- bdist（Build  Distribution）形式：ダウンロードして展開
- sdist（Source Distribution）形式：ダウンロードして展開してsetup.pyを実行

パッケージのインストール元は以下

- PyPI (and other indexes) using requirement specifiers.
- VCS project urls.
- Local project directories.
- Local or remote source archives.
- “requirements files”：再現したいプロジェクト全体の依存関係を記載したファイル（`requirements.txt`, `pyproject.toml`）

`pip install` の処理フロー

1. Identify the base requirements. The user supplied arguments are processed here.
2. Resolve dependencies. What will be installed is determined here.
3. Build wheels. All the dependencies that can be are built into wheels.
4. Install the packages (and uninstall anything being upgraded/replaced).

Note that `pip install` prefers to leave the installed version as-is unless `--upgrade` is specified.

引数処理の順番

1. Project or archive URL.
2. Local directory (which must contain a `setup.py`, or pip will report an error).
3. Local file (a sdist or wheel format archive, following the naming conventions for those formats).
4. A requirement, as specified in **[PEP 440](https://peps.python.org/pep-0440/)**.

Each item identified is added to the set of requirements to be satisfied by the install.

## pipenv

参考：[公式リポジトリ](https://github.com/pypa/pipenv)

> It automatically creates and manages a virtualenv for your projects, as well as adds/removes packages from your `Pipfile` as you install/uninstall packages. It also generates the ever important `Pipfile.lock`, which is used to produce deterministic builds.
> 
- 仮想環境の作成とモジュールのインストールをうまいことやってくれる
- ビルドの再現性担保のために`Pipfile.lock`を作ってくれる→`Pipfile.lock`とpyenv x pipenv環境があれば簡単にプロジェクトを移行・開発ができる
    - ただのモジュールの羅列であった`requirements.txt`からの脱却

PyPaがpipを補完する目的で開発されており，当初サポートされていなかった依存関係の解決をサポートする

### How it works

- 仮想環境がないところで`pipenv install`を実行した時には，自動的に仮想環境を作成する
    - プロジェクトのルートディレクトリにそのパスのhash値を付け足した名前で`~/.local/share/virtualenvs`以下に保存される
    - `PIPENV_VENV_IN_PROJECT`に1を設定すると，プロジェクトのルートディレクトリ直下に置き場として`.env`を作成する
- `pipenv install`に引数を渡さなかった時には，`Pipfile`に記載されている[packages]で指定されているものをインストールする

パッケージのインストール方法について`pip install`と`pipenv install` は完全に互換している

`Pipfile.lock`はプロジェクトの依存する全てのパッケージと，それらの利用可能な最新のバージョン，ダウンロード済みのファイルの現在のハッシュ値がまとめられているjson形式のファイル．これのおかげでdeterministic buildが保障されている．ちなみに，ハッシュ値をローカルで計算することで信頼できないPyPIエンドポイントからのダウンロードやネットワーク上の脅威の元でも，意図したパッケージのインストールを担保できる．

### How  to use

以下pyenv導入済みの前提で記述する．

```bash
pip install pipenv
```

- 正しくpyenvと連携できているかは`pyenv which pipenv`として`$PYENV_ROOT/versions/x.x.x/bin/pipenv`となっていればOk
    
    もし違うものが出ている場合は環境変数`PIPENV_PYTHON`を`$PYENV_ROOT/shims/python`とすることでうまく紐づく
    

指定したpythonのバージョンをビルドして仮想環境を作るには以下

```bash
pipenv install --python <version>
```

- `pipenv shell`： サブシェルを立ち上げて仮想環境に入ることができる
    - 仮想環境のバイナリディレクトリを`$PATH`の先頭に追加してpythonコマンドで，仮想環境のPython interpreterが呼び出されるようになる．
- `pipenv run`：仮想環境でrun以降のコマンドを実行する
- `pipenv --rm`：仮想環境の削除．~/.local/share/virtualenvs/以下の対応する仮想環境が丸ごと削除される．PipfileとPipfile.lockは削除されないので適宜削除．
- `pipenv clean`： `Pipfile.lock`で指定されていないパッケージをアンインストールする
- `pipenv install`：`Pipfile`を元にパッケージのインストールを行う．新たなパッケージをインストールする時には`Pipfile`に追記する．
- `pipenv lock`：`Pipfile.lock`を作成する．途中で例外送出される場合には`--clear`をつけてキャッシュを削除する必要がある
- `pipenv update`:：パッケージの更新を行う．指定しなければ全てのパッケージを更新する

## poetry

参考：[公式リポジトリ](https://github.com/python-poetry/poetry)

> Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.


### How it works

### How to use
以下pyenv導入済みの前提で記述する．

```bash
pip install poetry
```

- 正しくpyenvと連携できているかは`pyenv which poetry`として`$PYENV_ROOT/versions/x.x.x/bin/pipenv`となっていればOk

紐づいたpythonのバージョンをビルドして仮想環境を作るには以下

```bash
poetry init
```

異なるpythonバージョンの環境を作りたい場合は，pyenvでバージョンを切り替えてから`poetry init`とすれば良い

- `pipenv shell`： サブシェルを立ち上げて仮想環境に入ることができる
    - 仮想環境のバイナリディレクトリを`$PATH`の先頭に追加してpythonコマンドで，仮想環境のPython interpreterが呼び出されるようになる．
- `pipenv run`：仮想環境でrun以降のコマンドを実行する
- `pipenv --rm`：仮想環境の削除．~/.local/share/virtualenvs/以下の対応する仮想環境が丸ごと削除される．PipfileとPipfile.lockは削除されないので適宜削除．
- `pipenv clean`： `Pipfile.lock`で指定されていないパッケージをアンインストールする
- `pipenv install`：`Pipfile`を元にパッケージのインストールを行う．新たなパッケージをインストールする時には`Pipfile`に追記する．
- `pipenv lock`：`Pipfile.lock`を作成する．途中で例外送出される場合には`--clear`をつけてキャッシュを削除する必要がある
- `pipenv update`:：パッケージの更新を行う．指定しなければ全てのパッケージを更新する