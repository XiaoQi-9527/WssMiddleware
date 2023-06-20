# -*- coding:utf-8 -*-
# @Author: Aiden
# @Date: 2023/6/15 13:20

import asyncio

from Models import SubscribeConfigModel


class Test:

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def func(self):
        a = ['ltc_usdt', 'btc_usdt', 'eth_usdt', 'aca_usdt', 'alpaca_usdt', 'ar_usdt', 'arpa_usdt', 'audio_usdt',
             'bnx_usdt', 'bsw_usdt', 'busd_usdt', 'c98_usdt', 'celo_usdt', 'dar_usdt', 'edu_usdt', 'egld_usdt',
             'epx_usdt', 'fida_usdt', 'flow_usdt', 'glmr_usdt', 'hot_usdt', 'icp_usdt', 'iost_usdt', 'joe_usdt',
             'kp3r_usdt', 'lit_usdt', 'mask_usdt', 'mbox_usdt', 'near_usdt', 'op_usdt', 'porto_usdt', 'qnt_usdt',
             'qtum_usdt', 'rad_usdt', 'ray_usdt', 'rdnt_usdt', 'reef_usdt', 'rndr_usdt', 'santos_usdt', 'scrt_usdt',
             'sfp_usdt', 'ssv_usdt', 'storj_usdt', 'sui_usdt', 'super_usdt', 'sys_usdt', 't_usdt', 'tlm_usdt',
             'twt_usdt', 'uma_usdt', 'waves_usdt', 'xec_usdt', 'xlm_usdt', 'xtz_usdt', 'zen_usdt', 'zil_usdt',
             'alice_usdt', 'amp_usdt', 'ankr_usdt', 'ant_usdt', 'apt_usdt', 'badger_usdt', 'bal_usdt', 'blz_usdt',
             'bnb_btc', 'bnb_eth', 'bnt_usdt', 'bts_usdt', 'cake_usdt', 'celr_usdt', 'chess_usdt', 'chz_usdt',
             'ckb_usdt', 'comp_usdt', 'crv_usdt', 'cvx_usdt', 'dash_usdt', 'dgb_usdt', 'dodo_usdt', 'dydx_usdt',
             'ens_usdt', 'eos_usdt', 'ern_usdt', 'etc_usdt', 'fet_usdt', 'fis_usdt', 'flm_usdt', 'fxs_usdt', 'gal_usdt',
             'gala_usdt', 'gmx_usdt', 'gns_usdt', 'grt_usdt', 'gmt_usdt', 'bel_usdt', 'gtc_usdt', 'hft_usdt',
             'hook_usdt', 'id_usdt', 'ilv_usdt', 'inj_usdt', 'jasmy_usdt', 'kava_usdt', 'lazio_usdt', 'lqty_usdt',
             'lrc_usdt', 'mkr_usdt', 'mob_usdt', 'movr_usdt', 'omg_usdt', 'osmo_usdt', 'paxg_usdt', 'perp_usdt',
             'pyr_usdt', 'qi_usdt', 'quick_usdt', 'ren_usdt', 'rif_usdt', 'rose_usdt', 'rvn_usdt', 'sand_usdt',
             'slp_usdt', 'snx_usdt', 'stx_usdt', 'sushi_usdt', 'syn_usdt', 'tomo_usdt', 'trx_btc', 'trx_eth',
             'trx_usdt', 'tvk_usdt', 'ustc_busd', 'utk_usdt', 'vgx_usdt', 'voxel_usdt', 'waxp_usdt', 'win_usdt',
             'woo_usdt', 'xrp_btc']
        # a = ["phb_busd"]
        # a = ["bch_usdt", "core_usdt", "crv_usdc", "ethw_usdt", "shib_usdc"]
        # a = ["dzoo_usdt", "elon_usdt", "ht_usdt", "mc_usdt", "nest_usdt"]

        ts = []
        for symbol in a:
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
