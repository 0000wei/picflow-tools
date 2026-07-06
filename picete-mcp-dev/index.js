#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ErrorCode,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import sharp from 'sharp';
import fs from 'fs/promises';
import path from 'path';

const server = new Server({
  name: 'picete-mcp',
  version: '1.1.0'
}, {
  capabilities: {
    tools: {}
  }
});

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'instagram-split',
        description: 'Split an image seamlessly for an Instagram carousel (max 10 tiles). Automatically center-crops to match the required aspect ratio.',
        inputSchema: {
          type: 'object',
          properties: {
            source: {
              type: 'string',
              description: 'Absolute path to the source image'
            },
            tiles: {
              type: 'number',
              description: 'Number of carousel tiles (1-10)',
              minimum: 1,
              maximum: 10
            },
            ratio: {
              type: 'string',
              description: 'Aspect ratio of each tile',
              enum: ['1:1', '4:5']
            }
          },
          required: ['source', 'tiles', 'ratio']
        }
      },
      {
        name: 'social-media-crop',
        description: 'Crop an image for social media platforms with safe zones (e.g. Facebook cover). Performs a smart center crop.',
        inputSchema: {
          type: 'object',
          properties: {
            source: {
              type: 'string',
              description: 'Absolute path to the source image'
            },
            platform: {
              type: 'string',
              description: 'Target platform and format',
              enum: ['facebook-cover-desktop', 'facebook-cover-mobile', 'twitter-header']
            }
          },
          required: ['source', 'platform']
        }
      }
    ]
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  
  if (name === 'instagram-split') {
    const { source, tiles, ratio } = args;
    if (!source || !tiles || !ratio) {
      throw new McpError(ErrorCode.InvalidParams, 'Missing required arguments');
    }
    if (tiles < 1 || tiles > 10) {
      throw new McpError(ErrorCode.InvalidParams, 'Tiles must be between 1 and 10');
    }
    
    let tileAspect;
    if (ratio === '1:1') tileAspect = 1;
    else if (ratio === '4:5') tileAspect = 4 / 5;
    else throw new McpError(ErrorCode.InvalidParams, 'Invalid ratio');
    
    const targetAspect = tileAspect * tiles;
    
    try {
      const image = sharp(source);
      const metadata = await image.metadata();
      
      let extractWidth = metadata.width;
      let extractHeight = metadata.height;
      
      const currentAspect = extractWidth / extractHeight;
      if (currentAspect > targetAspect) {
        // Image is too wide
        extractWidth = Math.round(extractHeight * targetAspect);
      } else {
        // Image is too tall
        extractHeight = Math.round(extractWidth / targetAspect);
      }
      
      // Center crop
      const left = Math.round((metadata.width - extractWidth) / 2);
      const top = Math.round((metadata.height - extractHeight) / 2);
      
      const cropped = image.extract({ left, top, width: extractWidth, height: extractHeight });
      
      const tileWidth = Math.round(extractWidth / tiles);
      const outputFiles = [];
      const parsedPath = path.parse(source);
      
      for (let i = 0; i < tiles; i++) {
        const outPath = path.join(parsedPath.dir, `${parsedPath.name}_part${i + 1}${parsedPath.ext}`);
        await cropped.clone().extract({
          left: i * tileWidth,
          top: 0,
          width: tileWidth,
          height: extractHeight
        }).toFile(outPath);
        outputFiles.push(outPath);
      }
      
      return {
        content: [{ type: 'text', text: `Successfully split image into ${tiles} tiles:\n${outputFiles.join('\n')}` }]
      };
    } catch (e) {
      throw new McpError(ErrorCode.InternalError, `Failed to process image: ${e.message}`);
    }
  } else if (name === 'social-media-crop') {
      const { source, platform } = args;
      if (!source || !platform) {
        throw new McpError(ErrorCode.InvalidParams, 'Missing required arguments');
      }
      
      try {
        const image = sharp(source);
        
        let targetWidth, targetHeight;
        
        if (platform === 'facebook-cover-desktop') {
            targetWidth = 820;
            targetHeight = 312;
        } else if (platform === 'facebook-cover-mobile') {
            targetWidth = 640;
            targetHeight = 360;
        } else if (platform === 'twitter-header') {
            targetWidth = 1500;
            targetHeight = 500;
        } else {
            throw new McpError(ErrorCode.InvalidParams, 'Unsupported platform');
        }
        
        const parsedPath = path.parse(source);
        const outPath = path.join(parsedPath.dir, `${parsedPath.name}_${platform}${parsedPath.ext}`);
        
        await image.resize({
            width: targetWidth,
            height: targetHeight,
            fit: 'cover',
            position: 'center'
        }).toFile(outPath);
        
        return {
            content: [{ type: 'text', text: `Successfully cropped image for ${platform}:\n${outPath}` }]
        };
      } catch (e) {
          throw new McpError(ErrorCode.InternalError, `Failed to process image: ${e.message}`);
      }
  }
  
  throw new McpError(ErrorCode.MethodNotFound, `Tool not found: ${name}`);
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('PicEte MCP Server running on stdio');
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
