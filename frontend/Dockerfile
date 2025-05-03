# Start with a base Node.js image
FROM node:18-alpine

<<<<<<< Updated upstream
# Set the working directory inside the container
WORKDIR /workspace
=======
# Install common build dependencies needed for some npm packages on Alpine
RUN apk add --no-cache python3 make g++

# Set the working directory inside the container
WORKDIR /app
>>>>>>> Stashed changes

# Copy the package.json and package-lock.json files into the container
COPY package*.json ./

<<<<<<< Updated upstream
# Install the Node.js dependencies
RUN npm install
=======
# Use npm ci or npm install
RUN npm ci --verbose # or RUN npm install --verbose
>>>>>>> Stashed changes

# Copy the entire frontend code into the container
# This will now copy the existing .cjs config files correctly
COPY . .

# Define the command to start the frontend development server
# Using host 0.0.0.0 allows connections from outside the container
<<<<<<< Updated upstream
CMD ["npm", "run", "dev"]
=======
CMD ["npm", "run", "dev", "--", "--host"]
>>>>>>> Stashed changes
