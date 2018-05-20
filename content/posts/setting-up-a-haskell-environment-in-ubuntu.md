Title: Setting up a Haskell Environment in Ubuntu
Category: Blog
Tags: haskell
Date: 05-14-2018 23:38:00
Modified: 05-19-2018 20:36:00

These instructions have been tested against Kubuntu 18.04 LTS.

In the process of learning Haskell, I've recently gone through the various editors to 
try and see which one has the ideal tooling. There's many different opinions on the matter, 
but for me I've settled on Emacs with intero. I went with intero because it has 
solid type-checking, an interactive REPL, and doesn't require a whole lot of configuration 
to get going. With that said, I'll show you how to setup this environment in the context of 
an Ubuntu system.

# Install Stack

The first thing we need to install is stack. If you come from a Node.js background then stack 
is somewhat akin to the functionality `nvm` and `npm` provide. Some of the most prominent features 
stack provides are dependency installation, scaffolding for new projects, and GHC version management.

To install stack, run the following command.

```bash
wget -qO- https://get.haskellstack.org/ | sh
```

Once installed, the `stack` binary will be available to use in your terminal. 

# Install Emacs

Installing Emacs in Ubuntu is a fairly trivial task that can be performed with the following command.

```bash
sudo apt-get install emacs
```

After installation, startup `emacs` at least once so that it initializes your `emacs.d` folder.

# Install Intero

Now before we install `intero` we also need install `libtinfo-dev`, without this package 
`intero` will fail to build with stack lts-11.

```bash
sudo apt-get install libtinfo-dev
```

Next place the following into `~/.emacs.d/init.el`.

```emacs-lisp
;; If you don't have MELPA in your package archives:
(require 'package)
(add-to-list
  'package-archives
  '("melpa" . "http://melpa.org/packages/") t)
(package-initialize)
(package-refresh-contents)

;; Install Intero
(package-install 'intero)
(add-hook 'haskell-mode-hook 'intero-mode)
```

With that file place, just open `emacs` in a terminal and `intero` should start installing.

# Create a Test Project

To verify that everything is working, create a new project with `stack`.

```bash
stack new test-project
cd test-project
stack setup
```

Now open `src/Lib.hs` and modify the code. You should see type errors come up as you change 
the file.

For more information on the rest of the features `intero` provides see the [repository](https://github.com/commercialhaskell/intero).

<br>