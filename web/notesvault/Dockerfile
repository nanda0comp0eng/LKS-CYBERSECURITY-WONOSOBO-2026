FROM node:18-alpine

# Create app directory
WORKDIR /app

# Create database directory
RUN mkdir -p /app/database

# Copy package files
COPY package*.json ./

# Install dependencies
RUN apk add --no-cache python3 make g++
RUN npm install

# Copy application files
COPY . .

# Copy and set up startup script
COPY start.sh .
RUN chmod +x start.sh

# Expose port
EXPOSE 3000

# Start application
CMD ["./start.sh"]
