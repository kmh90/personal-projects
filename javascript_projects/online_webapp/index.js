import express from "express";
import axios from "axios";
import bodyParser from "body-parser";

import { dirname } from "path";
import { fileURLToPath } from "url";

// General variables
const __dirname = dirname(fileURLToPath(import.meta.url));

const app = express();
const port = 3000;

// Application-used variables
const API_URL = "https://api.coinpaprika.com/v1";
const config = {
    headers: { 'Content-Type': 'application/json' },
};

// const coinList = '[{"id":"btc-bitcoin","name":"Bitcoin","symbol":"BTC","rank":1,"is_new":false,"is_active":true,"type":"coin"},{"id":"eth-ethereum","name":"Ethereum","symbol":"ETH","rank":2,"is_new":false,"is_active":true,"type":"coin"},{"id":"usdt-tether","name":"Tether","symbol":"USDT","rank":3,"is_new":false,"is_active":true,"type":"token"},{"id":"xrp-xrp","name":"XRP","symbol":"XRP","rank":4,"is_new":false,"is_active":true,"type":"coin"},{"id":"bnb-binance-coin","name":"BNB","symbol":"BNB","rank":5,"is_new":false,"is_active":true,"type":"coin"},{"id":"sol-solana","name":"Solana","symbol":"SOL","rank":6,"is_new":false,"is_active":true,"type":"coin"},{"id":"usdc-usd-coin","name":"USDC","symbol":"USDC","rank":7,"is_new":false,"is_active":true,"type":"token"},{"id":"doge-dogecoin","name":"Dogecoin","symbol":"DOGE","rank":8,"is_new":false,"is_active":true,"type":"coin"},{"id":"steth-lido-staked-ether","name":"Lido Staked Ether","symbol":"STETH","rank":9,"is_new":false,"is_active":true,"type":"token"},{"id":"trx-tron","name":"TRON","symbol":"TRX","rank":10,"is_new":false,"is_active":true,"type":"coin"},{"id":"ada-cardano","name":"Cardano","symbol":"ADA","rank":11,"is_new":false,"is_active":true,"type":"coin"},{"id":"wbtc-wrapped-bitcoin","name":"Wrapped Bitcoin","symbol":"WBTC","rank":12,"is_new":false,"is_active":true,"type":"token"},{"id":"hype-hyperliquid","name":"Hyperliquid","symbol":"HYPE","rank":13,"is_new":false,"is_active":true,"type":"coin"},{"id":"wsteth-wrapped-liquid-staked-ether-20","name":"Wrapped Liquid Staked Ether 2.0","symbol":"WSTETH","rank":14,"is_new":false,"is_active":true,"type":"token"},{"id":"bch-bitcoin-cash","name":"Bitcoin Cash","symbol":"BCH","rank":15,"is_new":false,"is_active":true,"type":"coin"},{"id":"sui-sui","name":"Sui","symbol":"SUI","rank":16,"is_new":false,"is_active":true,"type":"coin"},{"id":"weth-weth","name":"WETH","symbol":"WETH","rank":17,"is_new":false,"is_active":true,"type":"token"},{"id":"leo-leo-token","name":"LEO Token","symbol":"LEO","rank":18,"is_new":false,"is_active":true,"type":"token"},{"id":"link-chainlink","name":"Chainlink","symbol":"LINK","rank":19,"is_new":false,"is_active":true,"type":"token"},{"id":"btcb-binance-bitcoin","name":"Binance Bitcoin","symbol":"BTCB","rank":20,"is_new":false,"is_active":true,"type":"token"}]'

// const coinDetails = '[{"id":"btc-bitcoin","name":"Bitcoin","symbol":"BTC","parent":{"id":"eth-ethereum","name":"Ethereum","symbol":"ETH"},"rank":1,"is_new":false,"is_active":true,"type":"coin","logo":"https://static.coinpaprika.com/coin/bnb-binance-coin/logo.png","tags":[{"id":"blockchain-service","name":"Blockchain Service","coin_counter":160,"ico_counter":80}],"team":[{"id":"vitalik-buterin","name":"Vitalik Buterin","position":"Author"}],"description":"Bitcoin is a cryptocurrency and worldwide payment system. It is the first decentralized digital currency, as the system works without a central bank or single administrator.","message":"string","open_source":true,"hardware_wallet":true,"started_at":"2009-01-03T00:00:00Z","development_status":"Working product","proof_type":"Proof of work","org_structure":"Decentralized","hash_algorithm":"SHA256","contract":"string","platform":"string","contracts":[{"contract":"string","platform":"string","type":"string"}],"links":{"explorer":["http://blockchain.com/explorer","https://blockchair.com/bitcoin/blocks","https://blockexplorer.com/","https://live.blockcypher.com/btc/"],"facebook":["https://www.facebook.com/bitcoins/"],"reddit":["https://www.reddit.com/r/bitcoin"],"source_code":["https://github.com/bitcoin/bitcoin"],"website":["https://bitcoin.org/"],"youtube":["https://www.youtube.com/watch?v=Um63OQz3bjo"],"medium":null},"links_extended":[{"url":"http://blockchain.com/explorer","type":"explorer"},{"url":"https://www.reddit.com/r/bitcoin","type":"reddit","stats":{"subscribers":1009135}},{"url":"https://github.com/bitcoin/bitcoin","type":"source_code","stats":{"contributors":730,"stars":36613}},{"url":"https://bitcoin.org/","type":"website"}],"whitepaper":{"link":"https://static.coinpaprika.com/storage/cdn/whitepapers/215.pdf","thumbnail":"https://static.coinpaprika.com/storage/cdn/whitepapers/217.jpg"},"first_data_at":"2018-10-03T11:48:19Z","last_data_at":"2019-05-03T11:00:00"}]'

let mainJSONcoinList;
let searchText = "";
let filteredCoinList;
let imageExists = false;

let maxItemsPerPage = 10;
let pageNumDataMap = {
    pageNumbers: 1,
    currentPageNum: 1,
    pageNumLimit: 2
};

app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: true }));

// Functions
function getTotalPageNumbers(totalNumOfItems, itemsPerPage) {
    let quotient = Math.floor(totalNumOfItems / itemsPerPage);
    let remainder = totalNumOfItems % itemsPerPage;

    if (remainder === 0) {
        return quotient;
    } else {
        return quotient + 1;
    }
}

app.get("/", (req, res) => {
    res.render("index.ejs");
});

app.get("/about", (req, res) => {
    res.render("about.ejs");
});

app.get("/faqs", (req, res) => {
    res.render("faq.ejs");
});

app.get("/cryptocurrencies", async (req, res) => {

    const currPageNum = parseInt(req.query.page) || 1;
    searchText = req.query.search;
    let finalCoinList;
    
    if (searchText) {
        console.log("Searching for entries with " + searchText + "...");
        filteredCoinList = mainJSONcoinList.filter(coin => coin.name.toLowerCase().includes(searchText));
        finalCoinList = filteredCoinList;
    } else {
        try {
            let result = await axios.get(API_URL + "/coins");
            // console.log(result.data);
            mainJSONcoinList = result.data;
            finalCoinList = mainJSONcoinList
        } catch (error) {
            res.render("crypto.ejs", { error: JSON.stringify(error) });
        }
    }

    let dissectedCoinList = finalCoinList.slice((currPageNum - 1) * maxItemsPerPage, currPageNum * maxItemsPerPage);

    pageNumDataMap.currentPageNum = currPageNum;
    pageNumDataMap.pageNumbers = getTotalPageNumbers(finalCoinList.length, maxItemsPerPage);
    // console.log(pageNumDataMap);

    if (dissectedCoinList.length === 0) {
        res.render("crypto.ejs");
    } else {
        // console.log(dissectedCoinList);
        res.render("crypto.ejs", { data: dissectedCoinList, searchTerm: searchText, pageNumData: pageNumDataMap });
    }
});

app.get("/cryptocurrencies/:id", async (req, res) => {
    const itemId = req.params.id;
    try {
        const result = await axios.get(API_URL + `/coins/${itemId}`);
        let coinDetails = result.data;
        // console.log(coinDetails);

        if (!coinDetails) {
            res.render("coin.ejs");
        } else {
            console.log(coinDetails);
            res.render("coin.ejs", { data: coinDetails });
        }
    } catch (error) {
        res.render("coin.ejs", { error: JSON.stringify(error.response.data) });
    }
});


app.post("/cryptocurrencies", async (req, res) => {
    searchText = req.body.search.toLowerCase();
    console.log("User is searching for entries with text: " + searchText);
    res.redirect("/cryptocurrencies?search=" + searchText);
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
