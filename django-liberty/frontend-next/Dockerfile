FROM node:22

WORKDIR /app

RUN npm install -g bun
RUN npm install -g pnpm

COPY src .

RUN bun install

EXPOSE 3000

CMD ["bun", "run", "dev"]
