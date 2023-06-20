const base = {
    cwd: "/root/WssMiddleware",
    interpreter: "/root/anaconda3/envs/CexMM/bin/python",
    args: "",
    namespace: "SpotWss",
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: "200M",
    log_date_format: "YYYY-MM-DD HH:mm:ss",
    ignore_watch: "/root/WssMiddleware/logs",
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
            name: "SpotWssBinance",
            script: "/root/WssMiddleware/App/public/binance_wss.py",
            out_file: "/root/WssMiddleware/logs/pm2/SpotWssBinance.out.log",
            error_file: "/root/WssMiddleware/logs/pm2/SpotWssBinance.error.log",
            ...base,
        },
        {
            name: "SpotWssGate",
            script: "/root/WssMiddleware/App/public/gate_wss.py",
            out_file: "/root/WssMiddleware/logs/pm2/SpotWssGate.out.log",
            error_file: "/root/WssMiddleware/logs/pm2/SpotWssGate.error.log",
            ...base,
        },
        {
            name: "SpotWssOkex",
            script: "/root/WssMiddleware/App/public/okex_wss.py",
            out_file: "/root/WssMiddleware/logs/pm2/SpotWssOkex.out.log",
            error_file: "/root/WssMiddleware/logs/pm2/SpotWssOkex.error.log",
            ...base,
        },
        {
            name: "SpotWssLbk",
            script: "/root/WssMiddleware/App/public/lbk_wss.py",
            out_file: "/root/WssMiddleware/logs/pm2/SpotWssLbk.out.log",
            error_file: "/root/WssMiddleware/logs/pm2/SpotWssLbk.error.log",
            ...base,
        },
    ]
}
