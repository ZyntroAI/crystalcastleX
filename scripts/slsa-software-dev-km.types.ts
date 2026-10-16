/**
 * SLSA Generic Data Schema v1.0.0
 * Software Development Lifecycle + Full Knowledge Management
 * Converted from JSON Schema Draft 2020-12
 */

// ============================================================
// BASE ENUMS
// ============================================================

export type SLSALevel = 'SLSA-0' | 'SLSA-1' | 'SLSA-2' | 'SLSA-3' | 'SLSA-4';
export type ComplianceStatus = 'met' | 'partial' | 'not-met';
export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';
export type VCSType = 'git' | 'svn' | 'mercurial' | 'other';
export type BuilderType = 'github-actions' | 'gitlab-ci' | 'jenkins' | 'tekton' | 'custom';
export type BuildType = 'snapshot' | 'release' | 'candidate';
export type StepStatus = 'success' | 'failed' | 'skipped';
export type SeverityLevel = 'low' | 'medium' | 'high' | 'critical';
export type TestType = 'unit' | 'integration' | 'e2e' | 'security' | 'performance' | 'compliance';
export type Environment = 'dev' | 'staging' | 'production' | 'sandbox';
export type KnowledgeStorageType = 'obsidian' | 'confluence' | 'git-wiki' | 'docs-as-code' | 'graph' | 'vector-db' | 'triple-store';
export type AccessPolicy = 'public' | 'internal' | 'team' | 'restricted' | 'classified';
export type KnowledgeDomain = 'architecture' | 'security' | 'devops' | 'coding-patterns' | 'troubleshooting' | 'compliance' | 'requirements' | 'testing' | 'deployment';
export type KnowledgeEntryType = 'concept' | 'procedure' | 'troubleshooting' | 'best-practice' | 'reference' | 'tutorial' | 'case-study' | 'lesson-learned' | 'faq' | 'decision-record';
export type EntryImportance = 'core' | 'supporting' | 'supplemental';
export type CaptureSource = 'code-comments' | 'pr-description' | 'commit-message' | 'issue' | 'meeting-minutes' | 'incident-report' | 'design-doc' | 'retrospective' | 'manual-input' | 'automated-analysis';
export type CaptureMechanism = 'manual' | 'template' | 'cli-tool' | 'webhook' | 'ai-assisted' | 'automated-pipeline';
export type KnowledgeRole = 'domain-expert' | 'developer' | 'tech-writer' | 'architect' | 'automation';
export type OrganizationMethod = 'folder-hierarchy' | 'tagging' | 'alias' | 'dataview-query' | 'graph-relation' | 'full-text-index' | 'semantic-embedding';
export type LinkingStrategy = 'explicit-hyperlink' | 'wiki-style-reference' | 'semantic-relation' | 'automated-backlink' | 'property-based-query';
export type RelationType = 'is-prerequisite-for' | 'relates-to' | 'supersedes' | 'supports' | 'contradicts' | 'implements' | 'references' | 'resolves';
export type ReviewProcess = 'peer-review' | 'expert-approval' | 'automated-check' | 'community-vote' | 'temporal-expiry';
export type DiscoveryMechanism = 'search' | 'browse-moc' | 'related-articles' | 'contextual-suggestion' | 'ai-query' | 'notification';
export type ArchiveStrategy = 'mark-deprecated' | 'move-to-archive' | 'delete-permanent' | 'migrate-to-new-location';
export type CodeRelationType = 'documented-by' | 'implements' | 'example-of' | 'fixed-in' | 'causes';
export type ResolutionType = 'root-cause' | 'workaround' | 'prevention-guide';
export type StandardRef = 'SLSA' | 'ISO27001' | 'NIST-SP800-53' | 'SOC2' | 'OWASP';
export type ArtifactType = 'container-image' | 'binary' | 'library' | 'sbom' | 'provenance' | 'attestation' | 'documentation' | 'source-archive' | 'test-report';
export type DigestAlgorithm = 'sha-256' | 'sha-512' | 'sha3-256' | 'sha3-512';
export type OwnerRole = 'maintainer' | 'contributor' | 'owner' | 'auditor';
export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced' | 'expert';
export type SchemaDomain = 'software-development' | 'devsecops' | 'knowledge-management' | 'supply-chain-security';

// ============================================================
// META & IDENTITY
// ============================================================

export interface SchemaMetadata {
  schemaVersion: '1.0.0';
  createdAt: string; // ISO 8601 date-time
  domain: SchemaDomain;
  specReference?: string;
}

export interface ProjectOwner {
  id: string;
  name: string;
  email?: string;
  role: OwnerRole;
}

export interface ProjectIdentity {
  projectId: string; // UUID
  name: string;
  description?: string;
  repoUri: string;
  vcsType?: VCSType;
  issueTrackerUri?: string;
  documentationUri?: string;
  owners: ProjectOwner[];
}

// ============================================================
// SLSA COMPLIANCE
// ============================================================

export interface RequirementStatus {
  level: string;
  requirement: string;
  status: ComplianceStatus;
  evidenceRef?: string;
}

export interface SLSARequirements {
  build?: RequirementStatus[];
  source?: RequirementStatus[];
  provenance?: RequirementStatus[];
}

export interface AttestationPoint {
  stage: string;
  attestationType: string;
  verificationMethod: string;
  publicKeyRef?: string;
}

export interface SLSACompliance {
  currentLevel: SLSALevel;
  targetLevel: SLSALevel;
  requirements: SLSARequirements;
  attestationPoints?: AttestationPoint[];
  riskAssessment?: RiskLevel;
  lastAuditDate?: string;
  nextAuditDate?: string;
}

// ============================================================
// SOFTWARE LIFECYCLE — SOURCE, BUILD, TEST, DEPLOY
// ============================================================

export interface ChangeHistoryEntry {
  commitHash: string;
  author: string;
  timestamp: string;
  message: string;
  knowledgeTags: string[];
  relatedDocs?: string[];
}

export interface SourceControl {
  commitHash: string;
  branch: string;
  tag: string;
  changeHistory: ChangeHistoryEntry[];
  accessControls?: {
    branchProtection?: boolean;
    signedCommitsRequired?: boolean;
    reviewRequired?: boolean;
  };
}

export interface BuilderInfo {
  id: string;
  type: BuilderType;
  version: string;
  uri?: string;
}

export interface BuildStep {
  stepName: string;
  executedAt: string;
  status: StepStatus;
  logsUri?: string;
  knowledgeRef?: string[];
}

export interface VulnerabilityInfo {
  cveId?: string;
  severity?: SeverityLevel;
  fixAvailable?: boolean;
  knowledgeEntry?: string;
}

export interface DependencyInfo {
  name: string;
  version: string;
  purl: string;
  integrityHash: string;
  source?: string;
  license?: string;
  vulnerabilities?: VulnerabilityInfo[];
}

export interface BuildProcess {
  builder: BuilderInfo;
  buildType: BuildType;
  buildInvocationUri: string;
  startedAt?: string;
  finishedAt?: string;
  steps: BuildStep[];
  dependencies?: DependencyInfo[];
  reproducible?: boolean;
}

export interface TestSuite {
  suiteId: string;
  type: TestType;
  totalTests: number;
  passed: number;
  failed: number;
  skipped?: number;
  executedAt: string;
  reportUri?: string;
  linkedKnowledge?: string[];
}

export interface CoverageInfo {
  lineCoveragePercent?: number;
  branchCoveragePercent?: number;
  reportUri?: string;
}

export interface StaticAnalysisResult {
  tool?: string;
  issuesFound?: number;
  reportUri?: string;
  knowledgeBaseRef?: string;
}

export interface TestingPhase {
  testSuites: TestSuite[];
  coverage: CoverageInfo;
  staticAnalysis?: StaticAnalysisResult[];
}

export interface DeploymentRecord {
  environment: Environment;
  deployedAt: string;
  deployedBy: string;
  artifactDigest: string;
  rollbackAvailable?: boolean;
  rollbackTriggeredAt?: string;
  changeLogUri?: string;
}

export interface SoftwareLifecycle {
  sourceControl: SourceControl;
  buildProcess: BuildProcess;
  testing: TestingPhase;
  deployment: DeploymentRecord[];
}

// ============================================================
// KNOWLEDGE MANAGEMENT
// ============================================================

export interface KnowledgeBaseInfo {
  id: string; // UUID
  name: string;
  description?: string;
  storageType: KnowledgeStorageType;
  endpoint: string;
  versionControl?: boolean;
  linkedDataEnabled?: boolean;
  embeddingModel?: string;
  accessPolicy: AccessPolicy;
}

export interface TagDefinition {
  tagId: string;
  name: string;
  category: string;
  description: string;
  synonyms?: string[];
  relatedTags?: string[];
}

export interface MOCEntry {
  entryId: string;
  title: string;
  uri: string;
  type: KnowledgeEntryType;
  importance?: EntryImportance;
}

export interface MapOfContent {
  mocId: string;
  title: string;
  purpose: string;
  entries: MOCEntry[];
}

export interface Taxonomy {
  domains?: KnowledgeDomain[];
  tags?: TagDefinition[];
  moc?: MapOfContent[];
}

export interface KnowledgeCreator {
  id?: string;
  role: KnowledgeRole;
}

export interface KnowledgeCreation {
  sources: CaptureSource[];
  captureMechanism: CaptureMechanism;
  authors?: KnowledgeCreator[];
}

export interface KnowledgeCuration {
  organizationMethod: OrganizationMethod[];
  linkingStrategy: LinkingStrategy;
  relationTypes?: RelationType[];
}

export interface KnowledgeValidation {
  reviewProcess: ReviewProcess;
  validityPeriodDays: number;
  lastValidatedAt?: string;
  nextReviewDue?: string;
  confidenceScore?: number; // 0..1
}

export interface KnowledgeDissemination {
  discoveryMechanisms?: DiscoveryMechanism[];
  accessLevels?: {
    read?: 'public' | 'authenticated' | 'team' | 'owner';
    write?: 'authenticated' | 'team' | 'owner';
    admin?: 'owner';
  };
  usageMetrics?: {
    viewCount?: number;
    reuseCount?: number;
    feedbackScore?: number; // 0..5
  };
}

export interface KnowledgeRetirement {
  archiveStrategy?: ArchiveStrategy;
  retentionPolicyDays?: number;
  archiveUri?: string;
  supersededBy?: string[];
}

export interface KnowledgeLifecycle {
  creation: KnowledgeCreation;
  curation: KnowledgeCuration;
  validation: KnowledgeValidation;
  dissemination: KnowledgeDissemination;
  retirement: KnowledgeRetirement;
}

export interface CodeToKnowledgeMapping {
  codeRef: string;
  knowledgeEntryUri: string;
  relationType: CodeRelationType;
}

export interface IncidentToKnowledgeMapping {
  incidentId: string;
  knowledgeEntryUri: string;
  resolutionType: ResolutionType;
}

export interface ComplianceToKnowledgeMapping {
  standardRef: StandardRef;
  controlId: string;
  knowledgeEntryUri: string;
}

export interface SLSAToKnowledgeMapping {
  slsaLevel: string;
  requirementId: string;
  knowledgeEntryUri: string;
}

export interface KnowledgeMappings {
  codeToKnowledge?: CodeToKnowledgeMapping[];
  incidentToKnowledge?: IncidentToKnowledgeMapping[];
  complianceToKnowledge?: ComplianceToKnowledgeMapping[];
  slsaToKnowledge?: SLSAToKnowledgeMapping[];
}

export interface KnowledgeQualityMetrics {
  completenessScore?: number; // 0..1
  currencyScore?: number; // 0..1
  linkDensity?: number;
  orphanedEntries?: number;
  entriesDueReview?: number;
  coverageByDomain?: Partial<Record<KnowledgeDomain, number>>;
  searchSuccessRate?: number; // 0..1
  knowledgeReuseRate?: number; // 0..1
}

export interface UsageExample {
  context?: string;
  codeSnippetRef?: string;
  outcome?: string;
}

export interface KnowledgeEntry {
  entryId: string; // UUID
  title: string;
  aliases?: string[];
  contentType: KnowledgeEntryType;
  summary: string;
  bodyUri?: string;
  createdAt: string;
  updatedAt?: string;
  author: string;
  contributors?: string[];
  tags: string[];
  relatedEntries?: string[];
  prerequisites?: string[];
  difficultyLevel?: DifficultyLevel;
  validUntil?: string;
  confidenceScore?: number; // 0..1
  version?: string;
  slug?: string;
  frontmatter?: Record<string, unknown>;
  usageExamples?: UsageExample[];
  commonPitfalls?: string[];
  keywords?: string[];
}

export interface KnowledgeManagementSystem {
  knowledgeBase: KnowledgeBaseInfo;
  taxonomy: Taxonomy;
  knowledgeLifecycle: KnowledgeLifecycle;
  mappings: KnowledgeMappings;
  qualityMetrics: KnowledgeQualityMetrics;
  entries: KnowledgeEntry[];
}

// ============================================================
// ARTIFACTS & PROVENANCE
// ============================================================

export interface SoftwareArtifact {
  artifactId: string; // UUID
  name: string;
  version?: string;
  digest: string;
  digestAlgorithm: DigestAlgorithm;
  uri: string;
  type: ArtifactType;
  sbomRef?: string;
  attestationRefs?: string[];
  knowledgeDocs?: string[];
}

export interface ProvenanceSubject {
  uri: string;
  digest: Record<string, string>;
}

export interface ProvenanceMaterial {
  uri: string;
  digest: Record<string, string>;
}

export interface ProvenanceInvocation {
  configSource?: {
    uri?: string;
    digest?: Record<string, string>;
  };
  parameters?: Record<string, unknown>;
  environment?: Record<string, unknown>;
}

export interface ProvenanceMetadata {
  buildStartedOn?: string;
  buildFinishedOn?: string;
  completeness?: {
    parameters?: boolean;
    environment?: boolean;
    materials?: boolean;
  };
  reproducible?: boolean;
}

export interface SLSAProvenance {
  predicateType: 'https://slsa.dev/provenance/v1';
  subject: ProvenanceSubject[];
  buildType: string;
  materials: ProvenanceMaterial[];
  invocation?: ProvenanceInvocation;
  metadata?: ProvenanceMetadata;
}

// ============================================================
// ROOT INTERFACE
// ============================================================

export interface SLSASoftwareDevWithKM {
  schemaMetadata: SchemaMetadata;
  projectIdentity: ProjectIdentity;
  slsaCompliance: SLSACompliance;
  softwareLifecycle: SoftwareLifecycle;
  knowledgeManagement: KnowledgeManagementSystem;
  artifacts: SoftwareArtifact[];
  provenance: SLSAProvenance;
  extensions?: Record<string, unknown>;
}

export default SLSASoftwareDevWithKM;
