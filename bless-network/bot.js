import fs from "fs/promises";
import { HttpsProxyAgent } from "https-proxy-agent";
import chalk from "chalk";
import ora from "ora";
import inquirer from "inquirer";
import { Config } from "./config.js";

const apiBaseUrl = "https://gateway-run.bls.dev/api/v1";
const ipServiceUrl = "https://tight-block-2413.txlabs.workers.dev";
const MAX_PING_ERRORS = 3;
const pingInterval = 120000;
const restartDelay = 240000;
const processRestartDelay = 30000;

let useProxy;

const banner = `
 █████╗ ██╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗      █████╗ ███████╗ ██████╗
██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╔══██╗██╔════╝██╔════╝
███████║██║██████╔╝██║  ██║██████╔╝██║   ██║██████╔╝    ███████║███████╗██║     
██╔══██║██║██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝     ██╔══██║╚════██║██║     
██║  ██║██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║         ██║  ██║███████║╚██████╗
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝         ╚═╝  ╚═╝╚══════╝ ╚═════╝
                                                                                
====================================================
     BOT                : Blockless Bless Network Bot 
     Telegram Channel   : @airdropasc
     Telegram Group     : @autosultan_group
====================================================
`;

const displayHeader = () => {
  console.log(chalk.yellow(banner)); // Display the banner in yellow
};

const askAccountType = async () => {
  const answers = await inquirer.prompt([
    {
      type: "list",
      name: "accountType",
      message: "How many accounts would you like to use?",
      choices: ["Single Account", "Multiple Accounts"],
    },
  ]);

  console.log("");
  return answers.accountType;
};

// Function to ask about proxy usage
const askProxyMode = async () => {
  const answers = await inquirer.prompt([
    {
      type: "confirm",
      name: "useProxy",
      message: "Would you like to use proxies?",
      default: true,
    },
  ]);

  console.log("");
  return answers.useProxy;
};

const fetchIpAddress = async (fetch, agent) => {
  const spinner = ora(chalk.yellow("Fetching IP address...")).start();
  try {
    const response = await fetch(ipServiceUrl, { agent });
    const { ip } = await response.json();
    spinner.succeed(chalk.green(`IP fetched: ${ip}`));
    return ip;
  } catch (error) {
    spinner.fail(chalk.red("Failed to fetch IP address."));
    throw error;
  }
};

const registerNode = async (
  fetch,
  nodeId,
  hardwareId,
  ipAddress,
  agent,
  authToken
) => {
  const spinner = ora(chalk.yellow(`Registering node ${nodeId}...`)).start();
  try {
    const response = await fetch(`${apiBaseUrl}/nodes/${nodeId}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify({ ipAddress, hardwareId }),
      agent,
    });
    const data = await response.json();
    spinner.succeed(
      chalk.green(`Registration response: ${JSON.stringify(data)}`)
    );
    return data;
  } catch (error) {
    spinner.fail(chalk.red("Failed to register node."));
    throw error;
  }
};

const startSession = async (fetch, nodeId, agent, authToken) => {
  const spinner = ora(
    chalk.yellow(`Starting session for node ${nodeId}...`)
  ).start();
  try {
    const response = await fetch(
      `${apiBaseUrl}/nodes/${nodeId}/start-session`,
      {
        method: "POST",
        headers: { Authorization: `Bearer ${authToken}` },
        agent,
      }
    );
    const data = await response.json();
    spinner.succeed(
      chalk.green(`Start session response: ${JSON.stringify(data)}`)
    );
    return data;
  } catch (error) {
    spinner.fail(chalk.red("Failed to start session."));
    throw error;
  }
};

const pingNode = async (
  fetch,
  nodeId,
  agent,
  ipAddress,
  authToken,
  pingErrorCount
) => {
  const spinner = ora(chalk.yellow(`Pinging node ${nodeId}...`)).start();
  try {
    const response = await fetch(`${apiBaseUrl}/nodes/${nodeId}/ping`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${authToken}`,
        origin: "chrome-extension://pljbjcehnhcnofmkdbjolghdcjnmekia",
      },
      agent,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    spinner.succeed(
      chalk.green(
        `Ping response: ${
          data.status || "No status"
        }, NodeID: ${nodeId}, IP: ${ipAddress}`
      )
    );
    pingErrorCount[nodeId] = 0;
    return data;
  } catch (error) {
    spinner.fail(chalk.red("Failed to ping node."));
    console.error(chalk.red(`Error during ping: ${error.message}`));
    throw error;
  }
};
const activeNodes = new Set();
const nodeIntervals = new Map();

const processNode = async (node, agent, ipAddress, authToken) => {
  const pingErrorCount = {};
  let intervalId;

  while (true) {
    try {
      if (activeNodes.has(node.nodeId)) {
        console.log(
          chalk.yellow(
            `[${new Date().toISOString()}] Node ${
              node.nodeId
            } is already being processed.`
          )
        );
        return;
      }

      activeNodes.add(node.nodeId);
      console.log(
        chalk.blue(
          `[${new Date().toISOString()}] Processing nodeId: ${
            node.nodeId
          }, hardwareId: ${node.hardwareId}, IP: ${ipAddress}`
        )
      );

      await registerNode(
        fetch,
        node.nodeId,
        node.hardwareId,
        ipAddress,
        agent,
        authToken
      );
      await startSession(fetch, node.nodeId, agent, authToken);
      await pingNode(
        fetch,
        node.nodeId,
        agent,
        ipAddress,
        authToken,
        pingErrorCount
      );

      if (!nodeIntervals.has(node.nodeId)) {
        intervalId = setInterval(async () => {
          try {
            await pingNode(
              fetch,
              node.nodeId,
              agent,
              ipAddress,
              authToken,
              pingErrorCount
            );
          } catch (error) {
            console.error(
              chalk.red(
                `[${new Date().toISOString()}] Error during ping: ${
                  error.message
                }`
              )
            );
            pingErrorCount[node.nodeId] =
              (pingErrorCount[node.nodeId] ?? 0) + 1;

            if (pingErrorCount[node.nodeId] >= MAX_PING_ERRORS) {
              clearInterval(nodeIntervals.get(node.nodeId));
              nodeIntervals.delete(node.nodeId);
              activeNodes.delete(node.nodeId);
              console.error(
                chalk.red(
                  `[${new Date().toISOString()}] Ping failed ${MAX_PING_ERRORS} times for nodeId: ${
                    node.nodeId
                  }. Restarting process...`
                )
              );
              await new Promise((resolve) =>
                setTimeout(resolve, processRestartDelay)
              );
              await processNode(node, agent, ipAddress, authToken);
            }
            throw error;
          }
        }, pingInterval);
        nodeIntervals.set(node.nodeId, intervalId);
      }

      break; // Exit the loop if processing is successful
    } catch (error) {
      console.error(
        chalk.red(
          `[${new Date().toISOString()}] Error occurred for nodeId: ${
            node.nodeId
          }, restarting process in ${restartDelay / 1000} seconds: ${
            error.message
          }`
        )
      );
      await new Promise((resolve) => setTimeout(resolve, restartDelay));
    } finally {
      activeNodes.delete(node.nodeId);
    }
  }
};

const runAll = async (initialRun = true) => {
  try {
    if (initialRun) {
      await displayHeader();
      useProxy = await askProxyMode(); // Use inquirer instead of prompt-sync
    }

    const fetch = await import("node-fetch").then((module) => module.default);

    for (const user of Config) {
      for (const node of user.nodes) {
        const agent = useProxy ? new HttpsProxyAgent(node.proxy) : null;
        const ipAddress = useProxy ? await fetchIpAddress(fetch, agent) : null;

        processNode(node, agent, ipAddress, user.usertoken);
      }
    }
  } catch (error) {
    console.error(
      chalk.red(
        `[${new Date().toISOString()}] An error occurred: ${error.message}`
      )
    );
  }
};

process.on("uncaughtException", (error) => {
  console.error(
    chalk.red(
      `[${new Date().toISOString()}] Uncaught exception: ${error.message}`
    )
  );
  runAll(false);
});

runAll();
