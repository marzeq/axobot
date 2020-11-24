import discord
from discord.ext import commands
import json
import requests

class SkyBazar(commands.Cog):

    def __init__(self, client):
        self.client = client
        with open("config/hypixelapi.json", "r") as f:
            val = json.load(f)
            self.api_key = val["api_key"]

    def sbazaritem(self, item: str) -> dict:
        with open("config/sbitems.json", "r") as f:
            itemjson = json.load(f)
        for itemid in itemjson["items"]:
            if item.lower() in itemjson["items"][itemid] or itemid.lower().replace("_", " ") == item.lower() or itemid == item:
                request = requests.get(f"https://api.hypixel.net/skyblock/bazaar/product?productId={itemid}&key={self.api_key}").json()
                return request
        raise self.client.NoItemFound(f"This item doen't exist")

    @commands.command(aliases=["skybazaar"])
    async def skybazar(self, ctx: commands.Context, *, item: str):
        # Getting all translations
        lang = self.client.get_server_lang(ctx.guild)
        useful = lang["translations"]["bazaar"]
        result = self.sbazaritem(item)["product_info"]
        embed = discord.Embed(title=f"{useful['info']} {result['product_id']}").set_thumbnail(url="https://static.wikia"
                                                                                                  ".nocookie.net/hypixe"
                                                                                                  "l-skyblock/images/f/"
                                                                                                  "f0/Coins.png/revisio"
                                                                                                  "n/latest?cb=20191128"
                                                                                                  "043854")
        embed.add_field(name=f"*{useful['highest_buy_order']}:*",
                        value=f"""```    {useful['amount_ordered']}: {result['buy_summary'][0]["amount"]}
    {useful['price_per_unit']}: {result['buy_summary'][0]["pricePerUnit"]}
    {useful['in_orders'].format(result['buy_summary'][0]["orders"])}```""", inline=False)

        embed.add_field(name=f"*{useful['highest_sell_offer']}:*",
                        value=f"""```    {useful['amount_offered']}: {result['sell_summary'][0]["amount"]}
    {useful['price_per_unit']}: {result['sell_summary'][0]["pricePerUnit"]}
    {useful['in_offers'].format(result['sell_summary'][0]["orders"])}```""", inline=False)

        embed.add_field(name="*Other stats:*", value=f"""```    {useful['inst_buy']}: {round(result["quick_status"]["sellPrice"], 1)}*
    {useful['inst_sell']}: {round(result["quick_status"]["buyPrice"], 1)}*
    {useful['buy_volume']}: {result["quick_status"]["buyVolume"]}
    {useful['sell_volume']}: {result["quick_status"]["sellVolume"]}
    {useful['margin']}: {round(result['sell_summary'][0]["pricePerUnit"] - result['buy_summary'][0]["pricePerUnit"], 2)}```""", inline=False)
        embed.set_footer(text=useful["inaccurate"])
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(SkyBazar(client))


if __name__ == "__main__":
    import sys
    import os
    import pathlib
    os.chdir(f"{pathlib.Path(__file__).parent.absolute()}/..")
    os.system(f"{sys.executable} {pathlib.Path(__file__).parent.absolute()}/../main.py")
