import discord
from discord.ext import commands
import json
from api import *

bot = commands.Bot(command_prefix='!')

@bot.command()
async def check(ctx):
    try:
        sku_code = ctx.message.content.replace('!check ', '').strip()
        if sku_code == "":
            return
        stockX = StockX()
        product = stockX.searchProductBySkucode(sku_code=sku_code)
        if len(product) == 0:
            raise Exception("No result by search.")
        childrens = stockX.getProductInfoByUrlKey(urlKey=product[0]["urlKey"])
        if len(childrens) == 0:
            raise Exception("{sku_code} has no children.".format(sku_code=sku_code))
        embed = discord.Embed(title="**{sku_code} Stock information**".format(sku_code=sku_code))
        embed.set_thumbnail(url=product[0]["image_url"])
        embed.add_field(name="retailPrice", value="$" + str(childrens[0]["retailPrice"]), inline=False)
        embed.set_footer(text="Copb stockx", icon_url="https://i.imgur.com/dMo4ZGN.png")

        count = 1
        for children in childrens:
            embed.add_field(name="size {size}".format(size=children["size"]), value="HK$" + str(int(children["lowestAsk"])), inline=(count%3!=0))
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("[error]%s" % e)
if __name__ == '__main__':
    bot.run('token')
