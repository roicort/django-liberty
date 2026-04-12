FROM node:22 AS builder

WORKDIR /app

RUN npm install -g bun

COPY src .

RUN bun install
#RUN bun run build

# Use a multi-stage build to keep the final image small
FROM node:22 AS runner

WORKDIR /app

RUN npm install -g bun

COPY --from=builder /app ./

EXPOSE 3000

CMD ["bun", "run", "dev"]