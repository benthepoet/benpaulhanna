Title: SDL2/C Primer
Category: Blog
Date: 01-06-2021 22:00:00
Modified: 01-06-2022 22:00:00
Status: Draft

# Ubuntu-based Linux
To get started with SDL2 on an Ubuntu-based distribution is fairly easy. With the following 
command we'll install the necessary build tools (gcc, make) along with SDL2.

```bash
sudo apt install build-essential libsdl2-2.0.0 libsdl2-dev 
```

# Windows
Windows requires a little more effort to setup but it isn't that bad. The easiest way 
to setup SDL2 for Windows is to use MSYS. MSYS is a collection of Unix tools for building 
software that have been ported to Windows.

To install MSYS you'll first want to install Chocolatey, a package manager for Windows. You can 
find the instructions for that [here](https://chocolatey.org/install). Once Chocolatey is installed we 
can install MSYS with the following command.

```bash
choco install msys2
```

After that go ahead and open an MSYS shell. From here we'll install the build tools and SDL2 into our MSYS 
installation.

```bash
pacman -Syu
pacman -S mingw-w64-x86_64-toolchain mingw-w64-x86_64-SDL2
```

Now if you open a PowerShell or Command Prompt you should see that commands like `gcc` and `make` are available.