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

    @commands.command()
    async def skybazar(self, ctx: commands.Context, *, item: str):
        # TODO: Translate this
        result = self.sbazaritem(item)["product_info"]
        embed = discord.Embed(title=f"Bazaar info for {result['product_id']}").set_thumbnail(url="https://static.wikia.nocookie.net/hypixel-skyblock/images/f/f0/Coins.png/revision/latest?cb=20191128043854")
        embed.add_field(name="**Highest buy order:**",
                        value=f"""```    Amound ordered: {result['buy_summary'][0]["amount"]}
    Price per unit: {result['buy_summary'][0]["pricePerUnit"]}
    In {result['buy_summary'][0]["orders"]} orders```""", inline=False)

        embed.add_field(name="*Highest sell offer:*",
                        value=f"""```    Amound offered: {result['sell_summary'][0]["amount"]}
    Price per unit: {result['sell_summary'][0]["pricePerUnit"]}
    In {result['sell_summary'][0]["orders"]} offers```""", inline=False)

        embed.add_field(name="*Other stats:*", value=f"""```    Instant buy price: {round(result["quick_status"]["sellPrice"], 1)}*
    Instant sell price: {round(result["quick_status"]["buyPrice"], 1)}*
    Buy volume: {result["quick_status"]["buyVolume"]}
    Sell volume: {result["quick_status"]["sellVolume"]}
    Margin: {round(result['sell_summary'][0]["pricePerUnit"] - result['buy_summary'][0]["pricePerUnit"], 2)}```""", inline=False)
        embed.set_footer(text="* Is inaccurate due to bazaar tax")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(SkyBazar(client))
