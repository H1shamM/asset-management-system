package com.assetmanagement.models;

import java.time.Instant;
import java.util.List;
import java.util.Map;

public class SecurityScanResult {

    private String assetId;
    private boolean isCompliant;
    public List<SecurityFinding> findings;
    public Instant scannedAt;
    public Map<String, Object> summary;

    public SecurityScanResult() {
    }

    public SecurityScanResult(String assetId, boolean isCompliant, List<SecurityFinding> findings, Instant scannedAt,
            Map<String, Object> summary) {
        this.assetId = assetId;
        this.isCompliant = isCompliant;
        this.findings = findings;
        this.scannedAt = scannedAt;
        this.summary = summary;
    }

    public String getAssetId() {
        return assetId;
    }

    public void setAssetId(String id) {
        this.assetId = id;
    }

    public boolean isCompliant() {
        return isCompliant;
    }

    public void setCompliant(boolean isCompliant) {
        this.isCompliant = isCompliant;
    }

    public List<SecurityFinding> getFindings() {
        return findings;
    }

    public void setFindings(List<SecurityFinding> findings) {
        this.findings = findings;
    }

    public Instant getScannedAt() {
        return scannedAt;
    }

    public void setScannedAt(Instant scannedAt) {
        this.scannedAt = scannedAt;
    }

    public Map<String, Object> getSummary() {
        return summary;
    }

    public void setSummary(Map<String, Object> summary) {
        this.summary = summary;
    }

}
