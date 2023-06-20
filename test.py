# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/6/15 13:20

import asyncio

from Models import SubscribeConfigModel


class Test:

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def func(self):
        b_lst = ['1inch_usdt', 'aca_usdt', 'alice_usdt', 'alpaca_usdt', 'amp_usdt', 'ankr_usdt', 'ant_usdt', 'apt_usdt', 'ar_usdt', 'arpa_usdt', 'audio_usdt', 'badger_usdt', 'bal_usdt', 'bel1_usdt', 'blz_usdt', 'bnb_btc', 'bnb_busd', 'bnb_eth', 'bnt_usdt', 'bnx_usdt', 'bsw_usdt', 'btc_busd', 'bts_usdt', 'busd_usdt', 'c98_usdt', 'cake_usdt', 'celo_usdt', 'celr_usdt', 'chess_usdt', 'chz_usdt', 'ckb_usdt', 'comp_usdt', 'crv_usdt', 'cvx_usdt', 'dai_usdt', 'dar_usdt', 'dash_usdt', 'dgb_usdt', 'dodo_usdt', 'dydx_usdt', 'edu_usdt', 'egld_usdt', 'ens_usdt', 'eos_usdt', 'epx_usdt', 'ern_usdt', 'etc_usdt', 'eth_busd', 'fet_usdt', 'fida_usdt', 'fis_usdt', 'flm_usdt', 'flow_usdt', 'fxs_usdt', 'gal_usdt', 'gala_usdt', 'glmr_usdt', 'gmt1_usdt', 'gmx_usdt', 'gns_usdt', 'grt_usdt', 'gtc_usdt', 'hft_usdt', 'hook_usdt', 'hot_usdt', 'icp_usdt', 'id_usdt', 'ilv_usdt', 'inj_usdt', 'iost_usdt', 'jasmy_usdt', 'joe_usdt', 'kava_usdt', 'kp3r_usdt', 'lazio_usdt', 'lit_usdt', 'lqty_usdt', 'lrc_usdt', 'ltc_usdt', 'lunc_busd', 'mask_usdt', 'matic_busd', 'mbox_usdt', 'mkr_usdt', 'mob_usdt', 'movr_usdt', 'near_usdt', 'omg_usdt', 'op_usdt', 'osmo_usdt', 'paxg_usdt', 'perp_usdt', 'phb_busd', 'porto_usdt', 'pyr_usdt', 'qi_usdt', 'qnt_usdt', 'qtum_usdt', 'quick_usdt', 'rad_usdt', 'ray_usdt', 'rdnt_usdt', 'reef_usdt', 'ren_usdt', 'rif_usdt', 'rndr_usdt', 'rose_usdt', 'rvn_usdt', 'sand_usdt', 'santos_usdt', 'scrt_usdt', 'sfp_usdt', 'shib_busd', 'slp_usdt', 'snx_usdt', 'sol_busd', 'ssv_usdt', 'storj_usdt', 'stx_usdt', 'sui_usdt', 'super_usdt', 'sushi_usdt', 'syn_usdt', 'sys_usdt', 't_usdt', 'tlm_usdt', 'tomo_usdt', 'trx_btc', 'trx_eth', 'trx_usdt', 'tvk_usdt', 'twt_usdt', 'uma_usdt', 'ustc_busd', 'utk_usdt', 'vgx_usdt', 'voxel_usdt', 'waves_usdt', 'waxp_usdt', 'win_usdt', 'woo_usdt', 'xec_usdt', 'xlm_usdt', 'xrp_btc', 'xrp_busd', 'xrp_eth', 'xtz_usdt', 'yfii_usdt', 'ygg_usdt', 'zec_usdt', 'zen_usdt', 'zil_usdt']
        o_lst = ['avax_usdc', 'babydoge_usdt', 'bch_usdc', 'bch_usdt', 'blur_usdt', 'btc_usdc', 'cfx_usdt', 'core_usdt', 'crv_usdc', 'doge_usdc', 'dot_usdc', 'efi_usdt', 'ens_usdc', 'eos_usdc', 'eth_usdc', 'ethw_usdt', 'fil_usdc', 'flr_usdt', 'ftm_usdc', 'ghst_usdt', 'hnt_usdt', 'lat_usdt', 'lhinu_usdt', 'ltc_usdc', 'magic_usdt', 'mina_usdt', 'near_usdc', 'nym_usdt', 'okb_usdt', 'pepe_usdt', 'polydoge_usdt', 'ron_usdt', 'rss3_usdt', 'samo_usdt', 'sand_usdc', 'shib_usdc', 'sol_usdc', 'ton_usdt', 'town_usdt', 'trx_usdc', 'usdc_usdt', 'ustc_usdt', 'velo_usdt', 'xch_usdt', 'xrp_usdc', 'zbc_usdt', 'ordi_usdt']
        g_lst = ['bonk_usdt', 'ceek_usdt', 'cro_usdt', 'dzoo_usdt', 'elon_usdt', 'gst1_usdt', 'gt_usdt', 'hero_usdt', 'ht_usdt', 'imx_usdt', 'itgr_usdt', 'lai_usdt', 'leo_usdt', 'mc_usdt', 'metis_usdt', 'nest_usdt', 'pawswap_usdt', 'pros_usdt', 'raca_usdt', 'sxp_usdt', 'torn_usdt', 'tt_usdt', 'ufo_usdt', 'yooshi_usdt', 'zks_usdt']
        l_lst = ['1inch_usdt', 'aca_usdt', 'alice_usdt', 'alpaca_usdt', 'amp_usdt', 'ankr_usdt', 'ant_usdt', 'apt_usdt', 'ar_usdt', 'arpa_usdt', 'audio_usdt', 'avax_usdc', 'babydoge_usdt', 'badger_usdt', 'bal_usdt', 'bch_usdc', 'bch_usdt', 'bel1_usdt', 'blur_usdt', 'blz_usdt', 'bnb_btc', 'bnb_busd', 'bnb_eth', 'bnt_usdt', 'bnx_usdt', 'bonk_usdt', 'bsw_usdt', 'btc_busd', 'btc_usdc', 'bts_usdt', 'busd_usdt', 'c98_usdt', 'cake_usdt', 'ceek_usdt', 'celo_usdt', 'celr_usdt', 'cfx_usdt', 'chess_usdt', 'chz_usdt', 'ckb_usdt', 'comp_usdt', 'core_usdt', 'cro_usdt', 'crv_usdc', 'crv_usdt', 'cvx_usdt', 'dai_usdt', 'dar_usdt', 'dash_usdt', 'dgb_usdt', 'dodo_usdt', 'doge_usdc', 'dot_usdc', 'dydx_usdt', 'dzoo_usdt', 'edu_usdt', 'efi_usdt', 'egld_usdt', 'elon_usdt', 'ens_usdc', 'ens_usdt', 'eos_usdc', 'eos_usdt', 'epx_usdt', 'ern_usdt', 'etc_usdt', 'eth_busd', 'eth_usdc', 'ethw_usdt', 'fet_usdt', 'fida_usdt', 'fil_usdc', 'fis_usdt', 'flm_usdt', 'flow_usdt', 'flr_usdt', 'ftm_usdc', 'fxs_usdt', 'gal_usdt', 'gala_usdt', 'ghst_usdt', 'glmr_usdt', 'gmt1_usdt', 'gmx_usdt', 'gns_usdt', 'grt_usdt', 'gst1_usdt', 'gt_usdt', 'gtc_usdt', 'hero_usdt', 'hft_usdt', 'hnt_usdt', 'hook_usdt', 'hot_usdt', 'ht_usdt', 'icp_usdt', 'id_usdt', 'ilv_usdt', 'imx_usdt', 'inj_usdt', 'iost_usdt', 'itgr_usdt', 'jasmy_usdt', 'joe_usdt', 'kava_usdt', 'kp3r_usdt', 'lai_usdt', 'lat_usdt', 'lazio_usdt', 'leo_usdt', 'lhinu_usdt', 'lit_usdt', 'lqty_usdt', 'lrc_usdt', 'ltc_usdc', 'ltc_usdt', 'lunc_busd', 'magic_usdt', 'mask_usdt', 'matic_busd', 'mbox_usdt', 'mc_usdt', 'metis_usdt', 'mina_usdt', 'mkr_usdt', 'mob_usdt', 'movr_usdt', 'near_usdc', 'near_usdt', 'nest_usdt', 'nym_usdt', 'okb_usdt', 'omg_usdt', 'op_usdt', 'osmo_usdt', 'pawswap_usdt', 'paxg_usdt', 'pepe_usdt', 'perp_usdt', 'phb_busd', 'polydoge_usdt', 'porto_usdt', 'pros_usdt', 'pyr_usdt', 'qi_usdt', 'qnt_usdt', 'qtum_usdt', 'quick_usdt', 'raca_usdt', 'rad_usdt', 'ray_usdt', 'rdnt_usdt', 'reef_usdt', 'ren_usdt', 'rif_usdt', 'rndr_usdt', 'ron_usdt', 'rose_usdt', 'rss3_usdt', 'rvn_usdt', 'samo_usdt', 'sand_usdc', 'sand_usdt', 'santos_usdt', 'scrt_usdt', 'sfp_usdt', 'shib_busd', 'shib_usdc', 'slp_usdt', 'snx_usdt', 'sol_busd', 'sol_usdc', 'ssv_usdt', 'storj_usdt', 'stx_usdt', 'sui_usdt', 'super_usdt', 'sushi_usdt', 'sxp_usdt', 'syn_usdt', 'sys_usdt', 't_usdt', 'tlm_usdt', 'tomo_usdt', 'ton_usdt', 'torn_usdt', 'town_usdt', 'trx_btc', 'trx_eth', 'trx_usdc', 'trx_usdt', 'tt_usdt', 'tvk_usdt', 'twt_usdt', 'ufo_usdt', 'uma_usdt', 'usdc_usdt', 'ustc_busd', 'ustc_usdt', 'utk_usdt', 'velo_usdt', 'vgx_usdt', 'voxel_usdt', 'waves_usdt', 'waxp_usdt', 'win_usdt', 'woo_usdt', 'xch_usdt', 'xec_usdt', 'xlm_usdt', 'xrp_btc', 'xrp_busd', 'xrp_eth', 'xrp_usdc', 'xtz_usdt', 'yfii_usdt', 'ygg_usdt', 'yooshi_usdt', 'zbc_usdt', 'zec_usdt', 'zen_usdt', 'zil_usdt', 'zks_usdt', 'ordi_usdt']

        # a = ["phb_busd"]
        # a = ["bch_usdt", "core_usdt", "crv_usdc", "ethw_usdt", "shib_usdc"]
        # a = ["dzoo_usdt", "elon_usdt", "ht_usdt", "mc_usdt", "nest_usdt"]

        ts = []
        for symbol in b_lst:
            ts.append({
                "symbol": symbol,
                "exchange": "binance",
                "type": "spot",
                "status": True,
                "business": "depth",
                "params": ""
            })
        for symbol in o_lst:
            ts.append({
                "symbol": symbol,
                "exchange": "okex",
                "type": "spot",
                "status": True,
                "business": "depth",
                "params": ""
            })
        for symbol in g_lst:
            ts.append({
                "symbol": symbol,
                "exchange": "gate",
                "type": "spot",
                "status": True,
                "business": "depth",
                "params": ""
            })
        for symbol in l_lst:
            ts.append({
                "symbol": symbol,
                "exchange": "lbank",
                "type": "spot",
                "status": True,
                "business": "depth",
                "params": ""
            })
        sql = SubscribeConfigModel.insert_many(ts)
        await SubscribeConfigModel().object.execute(sql)
        print("ok")

    def run(self):
        self.loop.run_until_complete(self.func())
        self.loop.run_forever()


if __name__ == "__main__":
    Test().run()
