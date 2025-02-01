# Установка базового образа
FROM node:18-alpine

# Установка рабочей директории
WORKDIR /app

# Копирование package.json и package-lock.json в рабочую директорию
COPY package*.json ./

# Установка зависимостей
RUN npm cache clean --force && rm -rf node_modules package-lock.json && npm install

# Копирование всех файлов в рабочую директорию
COPY . .

# Открытие порта
EXPOSE 3000

# Запуск Vite сервера
CMD ["npm", "run", "dev"]
