

[![N|Solid](/home/admincgn/securiteroutiere_CGN/cgn/deploy/pict/logo.png)]

## Containers and virtual machines

LXD provides support for system containers and virtual machines.
When running a system container, LXD simulates a virtual version of a full operating system. To do this, it uses the functionality provided by the kernel running on the host system.
When running a virtual machine, LXD uses the hardware of the host system, but the kernel is provided by the virtual machine. Therefore, virtual machines can be used to run, for example, a different operating system.

LXC is a userspace interface for the Linux kernel containment features. Through a powerful API and simple tools, it lets Linux users easily create and manage system or application containers.

### Virtual machines vs. system containers

Virtual machines emulate a physical machine, using the hardware of the host system from a full and completely isolated operating system. System containers, on the other hand, use the OS kernel of the host system instead of creating their own environment. If you run several system containers, they all share the same kernel, which makes them faster and more light-weight than virtual machines.
With LXD, you can create both system containers and virtual machines. You should use a system container to leverage the smaller size and increased performance if all functionality you require is compatible with the kernel of your host operating system. If you need functionality that is not supported by the OS kernel of your host system or you want to run a completely different OS, use a virtual machine.
___
## Features

#### Instances and profiles
-   [Image based](https://images.linuxcontainers.org/) (with images for a wide variety of Linux distributions, published daily)
-   [Containers](https://linuxcontainers.org/lxd/docs/master/containers) (the most complete implementation of LXD instances)
-   [Virtual machines](https://linuxcontainers.org/lxd/docs/master/virtual-machines) (implemented through the use of qemu)
-   [Configurable through profiles](https://linuxcontainers.org/lxd/docs/master/profiles) (applicable to both containers and virtual machines)

#### Backup and export
-   [Backup and recovery](https://linuxcontainers.org/lxd/docs/master/backup) (for all objects managed by LXD)
-   [Snapshots](https://linuxcontainers.org/lxd/docs/master/instances#snapshot-scheduling) (to save and restore the state of an instance)
-   [Container and image transfer](https://linuxcontainers.org/lxd/docs/master/image-handling) (between different hosts, using images)
-   [Live migration](https://linuxcontainers.org/lxd/docs/master/migration) (using CRIU)

#### Configurability
-   [Multiple storage backends](https://linuxcontainers.org/lxd/docs/master/explanation/storage/) (with configurable storage pools and storage volumes)
-   [Network management](https://linuxcontainers.org/lxd/docs/master/explanation/networks/) (including bridge creation and configuration, cross-host tunnels, ...)
-   [Advanced resource control](https://linuxcontainers.org/lxd/docs/master/instances/#resource-limits-via-limits-kernel-limit-name) (CPU, memory, network I/O, block I/O, disk usage and kernel resources)
-   [Device passthrough](https://linuxcontainers.org/lxd/docs/master/container-environment) (USB, GPU, unix character and block devices, NICs, disks and paths)
***
# Set up our infrastructure

On our infrastructure we will use Linux LXC/LXD Virtualization Environment.
We create two containers with Ubuntu 22.04 linux, So first of all the first container is the Core Application server and the second one is the Data Base Application server.

In order to be able to configure the host server as a virtualization server, we must configure the latter according to the tasks described below

> Setup timezone and date
> Configure static IP addres
> Install LXD Virtualization snap packet
> Configure ZFS Pool Storage to store our VM and Containers
> LXD Init to set up all the configuration
> Create profile for Bridged networking (the containers will appeare in the same LAN)

## Container creation
```sh
sudo snap install LXD
sudo nano /etc/cloud/cloud.cfg and  add network: {config: disabled}
sudo lxc image copy images:ubuntu/focal local: --alias ubuntu
lxc image list
launch ubuntu2204 CGN-Server
launch ubuntu2204 BDD
sudo lxc profile assign CGN-Server bridgedprofile
sudo lxc profile assign BDD bridgedprofile
```

## Our Inftastracture

![containers](/home/admincgn/securiteroutiere_CGN/cgn/deploy/pict/CGN_Containers.PNG)
