import click
import json_mng
import last_id
from colorama import Fore
from colorama import just_fix_windows_console
just_fix_windows_console()


@click.group()
def cli():
    pass


@cli.command()
def projects():
    data = json_mng.read_json()
    for project in data:
        print(
            f"{Fore.CYAN} {project['id']} - {project['name']} - {project['proj']} - {project['proj_desc']} - {project['price']} {Fore.RESET}")


@cli.command()
@click.option('--name', required=True, help='Client name')
@click.option('--proj', required=True, help='Project name')
@click.option('--proj_desc', required=True, help='Project description')
@click.option('--price', required=True, help='Project price')
@click.pass_context
def new(ctx, name, proj, proj_desc, price):
    data = json_mng.read_json()
    if not name or not proj or not proj_desc or not price:
        ctx.fail(Fore.YELLOW + 'All field are required.')
    else:
        data = json_mng.read_json()
        if (len(data) > 0):
            new_id = last_id.get(data) + 1
        else:
            new_id = 0
        new_user = {
            "id": new_id,
            "name": name,
            "proj": proj,
            "proj_desc": proj_desc,
            "price": price
        }
        data.append(new_user)
        json_mng.write_json(data)
        print(
            f"{Fore.GREEN} Client {name} successfully created with id {new_id} {Fore.RESET}")


@cli.command()
@click.argument('id', type=int)
def project(id):
    data = json_mng.read_json()
    project = next((x for x in data if x["id"] == id), None)
    if project is None:
        print(f'{Fore.YELLOW} Client with id {id} not found. {Fore.RESET}')
    else:
        print(
            f"{Fore.CYAN} { project['id']} - {project['name']} - {project['proj']} - {project['proj_desc']} - {project['price']} {Fore.RESET}")


@cli.command()
@click.argument('id', type=int)
def delete(id):
    data = json_mng.read_json()
    user = next((x for x in data if x["id"] == id), None)
    if user is None:
        print(f'{Fore.YELLOW} Client with id {id} not found. {Fore.RESET}')
    else:
        data.remove(user)
        json_mng.write_json(data)
        print(f'{Fore.GREEN} Client with id {id} successfully deleted. {Fore.RESET}')


@cli.command()
@click.argument('id', type=int)
@click.option('--name', help='Client name')
@click.option('--proj', help='Project name')
@click.option('--proj_desc', help='Project description')
@click.option('--price', help='Project price')
@click.pass_context
def update(ctx, id, name, proj, proj_desc, price):
    data = json_mng.read_json()
    for project in data:
        if project['id'] == id:
            if name is not None:
                project['name'] = name
            if proj is not None:
                project['proj'] = proj
            if proj_desc is not None:
                project['proj_desc'] = proj_desc
            if price is not None:
                project['price'] = price
            break
    json_mng.write_json(data)
    print(f'{Fore.GREEN} Client with id {id} successfully updated. {Fore.RESET}')


@cli.command()
@click.option('--confirm', prompt=f'{Fore.RED} Are you sure to delete all clients? y/n {Fore.RESET}')
def delete_all(confirm):
    clients_count = len(json_mng.read_json())
    if confirm == 'y':
        json_mng.write_json([])
        print(
            f'{Fore.GREEN} {clients_count} client(s) successfully deleted {Fore.RESET}')
    else:
        print(f'{Fore.GREEN} Nothing deleted. {Fore.RESET}')


if __name__ == '__main__':
    cli()
