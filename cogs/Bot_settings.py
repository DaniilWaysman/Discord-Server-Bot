from disnake.ext import commands
from disnake import Status
import disnake
import config


def get_prefix(bot, message):
    config_data = config.load_config()
    return config_data["PREFIX"]


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="префикс")
    async def prefix_manager(self, inter: disnake.ApplicationCommandInteraction):
        pass
    
    @prefix_manager.sub_command(name="изменить", description="Изменить префикс бота.")
    async def change_prefix(self, inter: disnake.ApplicationCommandInteraction, 
                            префикс: str = commands.Param(description="Укажите новый префикс.")
                            ):
        
        if inter.author.id != config.OWNER_ID:
            await inter.response.send_message("Ошибка: Только владелец может изменить префикс.", ephemeral=True)
            return

        config_data = config.load_config()
        
        if префикс == config_data["PREFIX"]:
            await inter.response.send_message("Ошибка: У меня уже стоит указанный вами префикс.", ephemeral=True)
        else:
            config_data["PREFIX"] = префикс
            config.save_config(config_data)
            self.bot.command_prefix = get_prefix

            await inter.response.send_message(f"Префикс изменён на `{префикс}`.")
    
    
    @commands.slash_command(name="статус")
    async def activity_manager(self, inter: disnake.ApplicationCommandInteraction):
        pass
    
    @activity_manager.sub_command(name="изменить", description="Изменить статус бота.")
    async def change_activity(self, inter: disnake.ApplicationCommandInteraction, 
                              статус: str = commands.Param(description="Выберите статус.", 
                                                           choices=[
                                                               "В сети",
                                                               "Неактивен",
                                                               "Не беспокоить"
                                                           ]
                                                           )):
        if inter.author.id != config.OWNER_ID:
            await inter.response.send_message("Ошибка: Только владелец может изменить статус.", ephemeral=True)
            return
        
        status_mapping = {
            "В сети": Status.online,
            "Неактивен": Status.idle,
            "Не беспокоить": Status.dnd
        }
        
        new_status = status_mapping[статус]
        current_status = inter.guild.me.status
        
        if current_status == new_status:
            await inter.response.send_message("Ошибка: У меня уже стоит указанный вами статус.", ephemeral=True)
        else:
            await self.bot.change_presence(status=status_mapping[статус])
            await inter.response.send_message(f"Статус бота изменен на `{статус}`.", ephemeral=True)


def setup(bot):
    bot.add_cog(Settings(bot))
