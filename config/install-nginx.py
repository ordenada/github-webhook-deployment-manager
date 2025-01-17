import os
import readline
import argparse
import pathlib

parser = argparse.ArgumentParser(
    description='Install the nginx config',
)

base_path = pathlib.Path('/etc/nginx/')

parser.add_argument(
    '-d',
    '--destination',
    dest='destination',
    help='The destination path',
    default=base_path.joinpath('sites-available').absolute(),
)

parser.add_argument(
    '-s',
    '--enabled-destination',
    dest='enabled_destination',
    help='The enabled destination path',
    default=base_path.joinpath('sites-enabled').absolute(),
)

parser.add_argument(
    '-H',
    '--host',
    dest='hostname',
    help='The public hostname',
    required=True,
)

parser.add_argument(
    '-P',
    '--port',
    dest='port',
    type=int,
    help='The public port',
    required=True,
)

parser.add_argument(
    '--no-symlink',
    dest='no_symlink',
    action='store_true',
    help='Do not make symlink',
)

parser.add_argument(
    '-n',
    '--dry-run',
    action='store_true',
    dest='dry_run',
    help='Simulate the installation without making changes',
)

parser.add_argument(
    '-q',
    '--quiet',
    dest='quiet',
    action='store_true',
    help='Suppress non-essential output',
)

args = parser.parse_args()

hostname: str = args.hostname
port: int = args.port


try:
    # Config the destination
    destination = pathlib.Path(args.destination)
    if not args.quiet:
        new_destination = input(f'Path destination ({destination}): ')
        if new_destination.strip():
            destination = pathlib.Path(new_destination.strip())
        print('Path:', destination.absolute())

    if not args.quiet:
        print()
    
    parent_destination = destination.parent
    if not args.quiet:
        print('Parent folder:', parent_destination)
        print()

        

    if not args.no_symlink:
        # Config the enabled destination
        # enabled_destination = pathlib.Path(args.enabled_destination)
        enabled_destination = parent_destination.joinpath('sites-enabled')
        
        if not args.quiet:
            new_enabled_destination: str = input(f'Path of the enabled destination ({enabled_destination}): ')
            if new_enabled_destination.strip():
                enabled_destination = pathlib.Path(new_enabled_destination)
            print('Path enabled:', enabled_destination)
except KeyboardInterrupt:
    print()
    exit(0)


# Load the nginx config and set the values
try:
    with open('nginx.conf', 'r') as file:
        content = file.read()
except Exception:
    print('Cannot read the file nginx.conf')
    exit()


content = content.replace('{hostname}', hostname)
content = content.replace('{port}', str(port))

if not args.quiet:
    print('nginx.conf file read')

# Save values in the destination
file_destination_path = destination.joinpath(f'{hostname}.conf')
if not destination.exists():
    print('Path does not exist:', destination.absolute())
    exit(1)

if args.dry_run:
    if not args.quiet:
        print('Simulate save in', file_destination_path.absolute())
else:
    try:
        with open(file_destination_path.absolute(), 'w+') as file:
            file.write(content)
            if not args.quiet:
                print('nginx config saved in', file_destination_path.absolute())
    except PermissionError:
        print('Permission error to write in', destination.absolute())
        exit(1)
    except Exception as err:
        print('Error to write in', file_destination_path.absolute(), err)
        exit(1)


# Make the symlink
if not args.no_symlink:
    if args.dry_run:
        if not args.quiet:
            print('Simulate creating symlink from',
                file_destination_path.absolute(),
                'to',
                enabled_destination.absolute())
    else:
        try:
            os.symlink(file_destination_path.absolute(), enabled_destination)
            if not args.quiet:
                print('Symlink created')
        except FileExistsError:
            print('Error. The symlink already exist')
            exit(1)
        except OSError as err:
            print('Error to create the symlink:', err)

        if not args.quiet:
            print('Symblink created')


# Done
if not args.quiet:
    print('nginx config created in:')
    print('Path:', destination)
    if not args.no_symlink:
        print('Symlink path:', enabled_destination)
