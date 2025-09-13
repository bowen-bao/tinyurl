# ----------------------------
# 1️⃣ Build Stage – Compile the React app
# ----------------------------
FROM node:18-alpine AS build

# Set working directory inside the container
WORKDIR /app

# Copy dependency manifests first (better build cache)
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy the rest of the source code
COPY . .

# Build the optimized static files
RUN npm run build
# --> creates a /app/build directory with static HTML/CSS/JS

# ----------------------------
# 2️⃣ Serve Stage – Nginx to serve the static files
# ----------------------------
FROM nginx:alpine

# Copy build output from the first stage into Nginx’s html folder
COPY --from=build /app/build /usr/share/nginx/html

# (Optional) Replace default nginx.conf with your own to handle SPA routing
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (HTTP)
EXPOSE 80

# Start Nginx in foreground (required in Docker)
CMD ["nginx", "-g", "daemon off;"]