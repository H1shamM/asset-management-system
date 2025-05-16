package com.assetmanagement.controllers;

import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.assetmanagement.models.SecurityFinding;
import com.assetmanagement.models.SecurityScanResult;

@RestController
@RequestMapping("/security")
public class SecurityController {

  private final Map<String, List<SecurityFinding>> db = Map.of(
      // pretend “OS” or “type” keyed databases
      "VM", List.of(
          new SecurityFinding("CVE-2024-1111", "Outdated hypervisor guest tools", "MEDIUM"),
          new SecurityFinding("CVE-2023-2222", "Guest-to-host escape possibility", "HIGH")),
      "Container", List.of(
          new SecurityFinding("CVE-2025-3333", "Unpatched container runtime bug", "HIGH"),
          new SecurityFinding("CVE-2023-4444", "Privilege escalation in entrypoint", "MEDIUM")));

  @PostMapping("/test")
  public ResponseEntity<?> addTestSecurity() {
    List<SecurityFinding> findings = Arrays.asList(
        new SecurityFinding("VULN-1", "First dummy vulnerability.", "HIGH"),
        new SecurityFinding("VULN-2", "Second dummy vulnerability.", "MEDUIM"));

    SecurityScanResult item = new SecurityScanResult(
        "VM-123",
        true,
        findings,
        Instant.now(),
        new HashMap<>() // empty metadata
    );
    return ResponseEntity.status(HttpStatus.CREATED).body(item);
  }

  /**
   * @param assetId
   * @return
   */
  @GetMapping("/scan/{assetId}")
  public ResponseEntity<SecurityScanResult> scanAsset(@PathVariable String assetId) {

    // 1) Simulate scan duration
    try {
      Thread.sleep(1000 + new Random().nextInt(2000));
    } catch (InterruptedException e) {
      e.printStackTrace();
    }

    String assetType = assetId.contains("container") ? "Container" : "VM";
    List<SecurityFinding> findings = new ArrayList<>(db.getOrDefault(assetType, List.of()));

    boolean compliant = findings.isEmpty();

    String highest = findings.stream()
        .map(f -> f.severity)
        .max(Comparator.comparingInt(this::severityRank))
        .orElse("NONE");
    Map<String, Object> summary = Map.of(
        "totalFindings", findings.size(),
        "highestSeverity", highest);

    SecurityScanResult result = new SecurityScanResult(
        assetId, compliant, findings, Instant.now(), summary);

    return ResponseEntity.ok(result);
  }

  private int severityRank(String sev) {
    return switch (sev) {
      case "LOW" -> 1;
      case "MEDIUM" -> 2;
      case "HIGH" -> 3;
      default -> 0;
    };
  }

  @GetMapping("/policy/{assetId}")
  public ResponseEntity<Boolean> checkPolicy(@PathVariable String assetId) {
    // Example: Asset must have "encrypted=true" tag
    return ResponseEntity.ok(assetId.endsWith("_encrypted"));
  }

}
