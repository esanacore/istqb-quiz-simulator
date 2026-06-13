import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, "..");

const server = new Server(
  {
    name: "istqb-quiz",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "istqb://data/questions",
        name: "ISTQB Question Bank",
        description: "The complete list of ISTQB practice questions",
        mimeType: "application/json",
      },
    ],
  };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  if (request.params.uri === "istqb://data/questions") {
    const content = await fs.readFile(path.join(PROJECT_ROOT, "question_bank.json"), "utf-8");
    return {
      contents: [
        {
          uri: request.params.uri,
          mimeType: "application/json",
          text: content,
        },
      ],
    };
  }
  throw new Error(`Resource not found: \${request.params.uri}`);
});

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_questions_by_topic",
        description: "Retrieves questions filtered by topic.",
        inputSchema: {
          type: "object",
          properties: {
            topic: {
              type: "string",
              description: "The topic to filter by (e.g., 'Testing Principles').",
            },
          },
          required: ["topic"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_questions_by_topic") {
    const { topic } = request.params.arguments;
    const content = await fs.readFile(path.join(PROJECT_ROOT, "question_bank.json"), "utf-8");
    const questions = JSON.parse(content);
    
    const filtered = questions.filter(q => q.topic && q.topic.includes(topic));
    
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(filtered, null, 2),
        },
      ],
    };
  }
  throw new Error(`Tool not found: \${request.params.name}`);
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("ISTQB Quiz MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});
