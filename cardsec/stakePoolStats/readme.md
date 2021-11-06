 <h1 align="center">Stake Pool Stats</h1>

  <h3 align="center">
  Mainnet
  </h3>
</div>

<details>
  <summary>Table of Contents</summary>
 <ol>
 <li><a href="#about=">About</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#steps-to-reproduce">Steps To Reproduce</a></li>
      </ul>
    </li>
 </ol>
</details>

## About

![stakePoolStats](https://raw.githubusercontent.com/SkryptLabs/Cardsec/main/cardsec/stakePoolStats/img/stakepoolstats.png)

If you are unfamiliar with the Cardano network. There are two types of nodes in the Cardano environment: block-producing nodes and relay nodes. The relays allows direct communication with the block producing node. These nodes are run by stake pool operators on various hosting providers. 

This pie chart represents data gathered and analysed from 2668 Cardano Mainnet Relays showing the distribution across various hosting providers. 
(Note: 2.8% of the data is not available in whois databases. Thus, represented by none in the given pie chart)


## Getting Started

Steps to analyse stake pool (mainnet/testent) yourself. The data was obtained through the Cardano GraphQL API which is available opensource [here](https://github.com/input-output-hk/cardano-graphql)

### Steps To Reproduce

1. Curl in terminal or extract from [here](https://graphql-api.mainnet.dandelion.link/) 

 ```
curl 'https://graphql-api.mainnet.dandelion.link/' -H 'Accept-Encoding: gzip, deflate, br' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Connection: keep-alive' -H 'DNT: 1' -H 'Origin: https://graphql-api.mainnet.dandelion.link' --data-binary '{"query":"{ stakePools{ id, url, relays {ipv4, dnsName, ipv6, dnsSrvName, port} }}\n"}'
 ```

Note: Change "mainnet" to "testnet", if you are analysing testnet.

2. Extract all the ips and resolve dns names.
 
3. Find whois records of all the ips. You can use this script to do a mass whois search.
   ```
   sudo apt-get install netcat
   ```
   ```
   wget https://raw.githubusercontent.com/SkryptLabs/Cardsec/main/cardsec/stakePoolStats/mass-whois.sh
   ```
   ```
   chmod +x mass-whois.sh
   ```
   ```
   ./mass-whois.sh [file containing ips]
   ```
   
