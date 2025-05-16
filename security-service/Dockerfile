# Stage 1: Build with Maven
FROM maven:3.9.6-eclipse-temurin-21 AS build

WORKDIR /app

# First copy only POM to cache dependencies
COPY pom.xml .
COPY config/ config/
# Download dependencies and plugins (verify before building)
RUN mvn verify clean --fail-never dependency:go-offline

# Copy source code
COPY src ./src

# Build application (include test phase for production)
RUN mvn clean package 

# Stage 2: Runtime image
FROM eclipse-temurin:21-jre-jammy

WORKDIR /app

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Copy built artifact
COPY --from=build --chown=appuser:appuser /app/target/security-service-*.jar ./app.jar

# Configure JVM
ENV JAVA_OPTS="-Djava.security.egd=file:/dev/./urandom -XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Debugging options (optional, remove for production)
ENV JAVA_DEBUG_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005"

# Entrypoint
ENTRYPOINT ["sh","-c","exec java $JAVA_OPTS $JAVA_DEBUG_OPTS -jar app.jar"]

# Document ports (actual exposure happens in compose)
EXPOSE 8080 5005