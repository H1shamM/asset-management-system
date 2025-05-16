package com.assetmanagement.models;

public class SecurityFinding {
    public String cveId;
    public String description;
    public String severity; // LOW, MEDIUM, HIGH

    public SecurityFinding(String cveId, String description, String severity) {
        this.cveId = cveId;
        this.description = description;
        this.severity = severity;
    }

    public String getCveId() {
        return cveId;
    }

    public void setCveId(String cveId) {
        this.cveId = cveId;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getSeverity() {
        return severity;
    }

    public void setSeverity(String severity) {
        this.severity = severity;
    }

}