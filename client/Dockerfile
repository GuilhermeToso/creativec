# Use the official Node.js 18 image as the base
FROM node:18-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV NEXT_PUBLIC_API_URL=http://creativec_backend:8000/api/v1

# Build the Next.js app
RUN npm run build

# Expose port 3000 to the outside world
EXPOSE 3000

# Start the Next.js app
CMD ["npm", "run", "start"]
