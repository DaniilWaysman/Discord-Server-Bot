import disnake
from disnake.ext import commands
from config import OWNER_ID


class EmbedGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="сгенерировать")
    async def create_embed(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @create_embed.sub_command(name="embed", description="Сгенерировать Embed сообщение.")
    async def generate_embed(
        self,
        inter: disnake.ApplicationCommandInteraction,
        заголовок: str = commands.Param(default=None, description="Заголовок Embed'а."),
        описание: str = commands.Param(default=None, description="Описание Embed'а."),
        цвет: str = commands.Param(
            choices=["Синий", "Красный", "Зелёный", "Жёлтый", "Фиолетовый", "Оранжевый", "Золотой", "По умолчанию"],
            description="Выбери цвет Embed'а"
        ),
    ):

        if inter.author.id != OWNER_ID:
            await inter.response.send_message("Ошибка: У вас недостаточно прав для использования..", ephemeral=True)
            return

        color_map = {
            "Синий": disnake.Color.blue(),
            "Красный": disnake.Color.red(),
            "Зелёный": disnake.Color.green(),
            "Жёлтый": disnake.Color.yellow(),
            "Фиолетовый": disnake.Color.purple(),
            "Оранжевый": disnake.Color.orange(),
            "Золотой": disnake.Color.gold(),
            "По умолчанию": disnake.Color.default()
        }

        embed_color = color_map.get(цвет, disnake.Color.default())

        embed = disnake.Embed(
            title=заголовок,
            description=описание,
            color=embed_color
        )
        
        embed.set_footer(text=f"Автор: {inter.author.display_name}", icon_url=inter.author.display_avatar.url)

        await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(EmbedGenerator(bot))
