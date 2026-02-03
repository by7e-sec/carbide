# CARBIDE

Carbide is a blueprint-based deployment system similar to Ansible that aims for simplicity and flexibility

## Basic overview

Example configuration is inside of `examples` folder, split in two sections:

### Config

`config` and `config-split` are providing same result while providing different approach to the configuration. While `config` provides all-in-one configuration file, while `config-split` provides split and seperate structure. It's possible mix-and-match the two.

### Blueprints

Blueprints are YAML-based configurations where you specify a single source (at the moment of writing that's only `local`) and possible multiple destinations.



## Installation

```
$ python -m venv ~/venvs/carbide
$ source ~/venvs/carbide/bin/activate
$ pip install -r requirements.txt
```

## Basic configuration

### carbide.yml
`/etc/carbide/carbide.yaml`
```yaml
blueprints:
  /path/to/your/blueprints

authentication:
  remote1:
    type: pass
    username: a_user
    password: default_password

machines:
  local:
    local: true

  remote1:
    hostname: 10.0.0.1
    authenticate: remote1

  remote2:
    hostname: 10.0.0.2
    authenticate: remote1

```

Note: Unless specified specifically through command line, carbide.yaml needs to be in one of the following folders (it's autodetected and in that order):

- /etc/carbide/
- ~/.local/share/carbide/
- ~/.carbide/
- ../config/
- ./config/
- ./


### Blueprint
`/path/to/your/blueprints/copy-to-remote.yaml`
```yaml
blueprint:
  description: Copy local->remote
  active: true
  logging: auto

  deploy:
    source:
      machine: local
      type: folder
      folder: /path/to/local/source/
      filter:
        - .git # ignores the .git folder and its content

    destinations:
      - machine: remote1
        folder: /path/to/remote/destination/
```

Done.

## Remote machine authentication

Carbide supports 2 types of authentication for machines inside of the `authentication` section:

- pass: username / password key pair
- ssh-key: SSH key authentication

### Examples

#### Username / password authentication

```yaml
  password:
    type: pass
    username: a_user
    password: default_password
```

#### Hardcoded SSH key authentication

```yaml
  sshkey:
    type: ssh-key
    username: a_user
    key_filename: ~/.ssh/id_rsa
    password: ssh_key_password
```

#### SSH key authentication through prompt

```yaml
  sshprompt:
    type: ssh-key
    username: a_user
    key_filename: ~/.ssh/id_rsa
    password: "{{$PROMPT}}"
```

#### SSH key authentication through environment

```yaml
  sshenv:
    type: ssh-key
    username: a_user
    key_filename: ~/.ssh/id_rsa
    password: "{{$ENV.PASS_FROM_ENVIRONMENT}}" # Variable after $ENV. can be completely custom
```

## Blueprints

Blueprints are the meat and potato of Carbide, and at the time of writing, it can only copy from local to remote machine via SFTP. Other modes (like rsync or NFS) are under development.

```yaml
blueprint:
  description: Copy local->remote
  active: true
  logging: auto

  deploy:
    source:
      machine: local
      type: folder
      folder: /path/to/local/source/
      filter:
        - .git # Ignores the .git folder and its contents

    destinations:
      - machine: remote1
        folder: /path/to/remote/folder/

    destinations:
      - machine: remote2
        folder: /path/to/remote/folder/
        run-commands-before:
          - service nginx stop
        run-commands-after:
          - service nginx start
```

Blueprints can be be deactivated by `active` switch (default is "active").

`description` provides a description of a blueprint inside of a command line. More information in [running-carbide](#running-carbide)

### Source

They take in a single source (currently only "local", but ability to have a remote machine is under development as well...)

`type` is type of content source; whether that's "files" or "folder", but currently only "folder" is supported.
`folder` is the source folder
`filter` filters out the folder / files that shouldn't be deployed. Filters are stackable


### Destinations

As the title implies, you can specify multiple destinations, consisting of machine name and destination folder.

`machine` handles the authentication, hostname (or IP) specified in `machines` section of `carbide.yaml` filename.

`folder` is the destination folder of the contents specified in `source`

`run-commands-before` and `run-commands-after` are directives that execute commands on (remote) machine before or after deployment respectively.

## Running Carbide

### Basic commands

``` bash
$ ./carbide.py --help
Usage: carbide.py [options]

Options:
  -h, --help            show this help message and exit
  -c CONFIG, --config=CONFIG
                        Path to config file
  -b BLUEPRINT, --blueprint=BLUEPRINT
                        Run specific blueprint (stackable)
  -l, --list            List available blueprints and exit
```

`-c ` offers an option to specify a custom path to carbide.yaml file

`-b ` offers an option to execute a single or a set of blueprints. By default Carbide executes all valid and active blueprints

`-l ` provides a list of blueprints, their status (active or invalid) and so on. Example:

```bash
$ ./carbide.py -l
Config found in ../config/carbide.yaml. Loading...
Available blueprints:
test-local-remote: Valid || Active
 Kind: sftp
 # Copy local->remote
 Destinations:
  > tea | Valid
  > forgy | Valid

test-remote-remote: Valid || Inactive
 Kind: sftp
 # Copy remote->remote
 Destinations:
  > remote3 | Not valid

test-local-local: Valid || Active
 Kind: local
 # Copy local->local
 Destinations:
  > local | Valid
  > remote1 | Not valid

```
