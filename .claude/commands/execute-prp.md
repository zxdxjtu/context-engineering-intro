# Execute BASE PRP

Implement a feature using using the PRP file.

## PRP File: $ARGUMENTS

## AI-Optimized Execution Process

1. **Load PRP & Axiom Context**
   - Read the specified PRP file
   - **FIRST**: Check `.axiom/index.yml` for project context and token budget
   - **Read relevant meta files** from `.axiom/meta/` to understand existing codebase
   - Follow all instructions in the PRP and extend research using meta summaries first
   - Use contracts (`.contract.yml`) to understand module interfaces before reading source code

2. **ULTRATHINK with AI Context**
   - Think hard before executing, leveraging AI-optimized context
   - Create comprehensive plan addressing all requirements AND meta maintenance
   - Use TodoWrite tool to track implementation plan INCLUDING meta file updates
   - Identify patterns from existing code via meta information first, source code second
   - Plan token-efficient implementation approach

3. **Execute with Meta Maintenance**
   - Execute the PRP implementation
   - **CRITICAL**: After EVERY file creation/modification, update corresponding meta file
   - Create `.contract.yml` files for new non-trivial modules
   - Maintain module size limits (< 200 lines for AI optimization)

4. **Validate & Sync**
   - Run each validation command specified in PRP
   - **REQUIRED**: Run `python3 scripts/axiom-meta-generator.py --scan` after major changes
   - Verify all meta files are synchronized
   - Check `.axiom/index.yml` sync_status is "clean"
   - Fix any failures and re-run until all pass

5. **Complete with Axiom Verification**
   - Ensure all checklist items done
   - **Verify meta consistency**: All source files have corresponding meta files
   - **Contract validation**: All contracts match actual implementation
   - **Token budget check**: Ensure new code fits within project token budget
   - Run final validation suite
   - Update `.axiom/index.yml` with final project state
   - Report completion status with meta sync confirmation

6. **Continuous Reference & Context**
   - Always reference the PRP for requirements
   - Use meta files for quick context instead of re-reading source code
   - Maintain AI context efficiency throughout development

## Axiom Protocol Requirements
- **Never commit** without updating meta files
- **Always create contracts** for complex modules  
- **Maintain token efficiency** - use meta summaries when possible
- **Verify sync status** before declaring task complete

Note: If validation fails, check meta files first, then use error patterns in PRP to fix and retry.