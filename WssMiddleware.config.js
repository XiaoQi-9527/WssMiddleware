const base = {
    cwd: "/root/WssMiddlewareV2",
    interpreter: "/root/anaconda3/envs/CexMM/bin/python",
    args: "",
    namespace: "SpotWssV2",
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: "200M",
    log_date_format: "YYYY-MM-DD HH:mm:ss",
    ignore_watch: "/root/WssMiddlewareV2/logs",
    min_uptime: "60s",
    max_restarts: 30,
    env: {
      NODE_ENV: "development",
    },
    env_production: {
      NODE_ENV: "production",
    },
};
module.exports = {
    apps:[
        {
            name: "SpotWssBinanceV2",
            script: "/root/WssMiddlewareV2/App/public/binance_wss.py",
            out_file: "/root/WssMiddlewareV2/logs/SpotWssBinance.out.log",
            error_file: "/root/WssMiddlewareV2/logs/SpotWssBinance.error.log",
            ...base,
        },
        {
            name: "SpotWssGateV2",
            script: "/root/WssMiddlewareV2/App/public/gate_wss.py",
            out_file: "/root/WssMiddlewareV2/logs/SpotWssGate.out.log",
            error_file: "/root/WssMiddlewareV2/logs/SpotWssGate.error.log",
            ...base,
        },
        {
            name: "SpotWssOkexV2",
            script: "/root/WssMiddlewareV2/App/public/okex_wss.py",
            out_file: "/root/WssMiddlewareV2/logs/SpotWssOkex.out.log",
            error_file: "/root/WssMiddlewareV2/logs/SpotWssOkex.error.log",
            ...base,
        },
        {
            name: "SpotWssLbkV2",
            script: "/root/WssMiddlewareV2/App/public/lbk_wss.py",
            out_file: "/root/WssMiddlewareV2/logs/SpotWssLbk.out.log",
            error_file: "/root/WssMiddlewareV2/logs/SpotWssLbk.error.log",
            ...base,
        },
    ]
}
