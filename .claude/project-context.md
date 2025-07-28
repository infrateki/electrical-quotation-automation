# 🏗️ Electrical Quotation System - Project Context

## 🎯 Business Domain Knowledge

### What is an Electrical Quotation?
An electrical quotation is a detailed document that outlines:
- **Scope of Work**: All electrical installations, upgrades, or repairs
- **Materials List**: Every component from panels to outlets with quantities
- **Labor Costs**: Hours and rates for different skill levels
- **Compliance**: NEC code requirements and local regulations
- **Timeline**: Project phases and milestones
- **Terms**: Payment schedules, warranties, change orders

### Key Stakeholders
1. **Electrical Contractors**: Primary users creating quotations
2. **General Contractors**: Receive quotations for larger projects  
3. **Property Owners**: Final decision makers
4. **Inspectors**: Verify NEC compliance
5. **Suppliers**: Provide material pricing

## 📊 Quotation Components Breakdown

### 1. Header Section
- Company logo and branding
- License numbers (critical for legitimacy)
- Contact information
- Quotation number and date
- Validity period (typically 30-60 days)

### 2. Client Information (To Section)
- Company/Individual name
- Project address (different from billing)
- Contact person
- Phone/Email
- Special requirements or preferences

### 3. Project Information
- **Project Type**: New construction, renovation, service upgrade
- **Square Footage**: Determines load calculations
- **Occupancy Type**: Residential, commercial, industrial
- **Special Requirements**: Hazardous locations, medical facilities
- **Phases**: Multiple stages for large projects

### 4. Line Items (Most Complex)
The heart of the quotation, organized by systems:

#### Essential Systems
- **Main Service**: Panel upgrades, meter installations
- **Distribution**: Subpanels, feeders, bus ducts
- **Grounding**: Equipment grounding, GFECs
- **Surge Protection**: Whole-building SPDs

#### Normal Power
- **Branch Circuits**: General outlets, dedicated circuits
- **Lighting Circuits**: Switches, dimmers, controls
- **Motor Circuits**: HVAC, pumps, equipment
- **Special Outlets**: Dryer, range, EV charging

#### Specialized Equipment
- **Data/Communications**: Network drops, fiber
- **Fire Alarm**: Detectors, pulls, panels
- **Security**: Cameras, access control
- **Audio/Visual**: Conference rooms, theaters

#### Backup Power
- **Generators**: Sizing, transfer switches
- **UPS Systems**: Critical loads, runtime
- **Emergency Lighting**: Exits, paths of egress
- **Solar/Battery**: Renewable integration

### 5. Pricing Summary
- **Materials Total**: With markup (typically 15-35%)
- **Labor Total**: Hours × rates by skill level
- **Equipment Rental**: Lifts, trenchers, etc.
- **Permits/Inspections**: Local fees
- **Subtotal**: Before taxes
- **Taxes**: State/local rates
- **Total**: Final quotation amount
- **Alternates**: Optional add-ons
- **Discounts**: Volume, repeat customer

### 6. Executive Summary
High-level overview for decision makers:
- Project understanding
- Key benefits/features
- Why choose this contractor
- Timeline highlights
- Investment summary

### 7. Terms & Conditions
- Payment schedule (typically 30/30/30/10)
- Change order process
- Warranty terms (1-2 years typical)
- Insurance and bonding
- Dispute resolution
- Material price escalation clauses

### 8. Approval Requirements
- Signature blocks
- Date fields
- Acceptance criteria
- Deposit requirements
- Notice to proceed

## 🔌 Electrical Domain Specifics

### Load Calculations (NEC 220)
```python
# Residential Load Calculation Example
general_lighting = square_feet * 3  # VA per sq ft
small_appliance = 1500 * 2  # Two circuits minimum
laundry = 1500  # One circuit minimum
total_general = general_lighting + small_appliance + laundry

# Apply demand factors
first_3000 = 3000 * 1.0
remaining = (total_general - 3000) * 0.35
calculated_load = first_3000 + remaining
```

### Voltage Drop Calculations (NEC 210.19)
- Maximum 3% for branch circuits
- Maximum 5% for feeders and branch combined
- Critical for long runs or sensitive equipment

### Conduit Fill (NEC Chapter 9)
- 40% fill for 3+ conductors
- Derating factors for multiple conductors
- Temperature corrections

### Circuit Breaker Sizing
- 125% continuous loads
- 100% non-continuous loads
- Ambient temperature corrections

## 💰 Pricing Intelligence

### Material Pricing Factors
1. **Market Volatility**: Copper prices fluctuate daily
2. **Quantity Breaks**: Bulk discounts at thresholds
3. **Manufacturer Relationships**: Contractor pricing tiers
4. **Lead Times**: Premium for quick delivery
5. **Regional Variations**: Local supply/demand

### Labor Pricing Structure
- **Journeyman**: $45-85/hour
- **Apprentice**: $25-45/hour  
- **Master/Foreman**: $65-110/hour
- **Overtime**: 1.5x after 8 hours, 2x Sundays
- **Prevailing Wage**: Government projects

### Markup Strategy
- **Materials**: 15-35% depending on:
  - Project size
  - Competition
  - Relationship
  - Risk factors
- **Labor**: 30-65% to cover:
  - Benefits
  - Insurance
  - Overhead
  - Profit

## 🏢 Project Types & Complexity

### Residential
- **Simple**: Service upgrades, panel replacements
- **Medium**: Whole house rewire, additions
- **Complex**: Smart homes, solar integration

### Commercial
- **Office**: Tenant improvements, lighting retrofits
- **Retail**: POS systems, display lighting
- **Restaurant**: Kitchen equipment, HVAC loads
- **Medical**: Isolated grounds, emergency power

### Industrial
- **Manufacturing**: Motor controls, high voltage
- **Warehouse**: High bay lighting, charging stations
- **Data Centers**: Redundant power, cooling
- **Hazardous**: Explosion-proof equipment

## 📏 NEC Compliance Critical Points

### 2023 NEC Major Changes
1. **GFCI Protection**: Expanded requirements
2. **Surge Protection**: Now required for dwellings
3. **Emergency Disconnects**: One/two family dwellings
4. **DC Microgrids**: New article 712
5. **EV Charging**: Updated requirements

### Common Violations to Check
- Improper grounding/bonding
- Insufficient working space
- Wrong wire sizing
- Missing disconnects
- Improper outdoor ratings

## 🔄 Workflow States

### Quotation Lifecycle
1. **Draft**: Initial creation, can be edited
2. **Review**: Internal QC, compliance check
3. **Submitted**: Sent to customer
4. **Negotiation**: Adjustments, alternatives
5. **Approved**: Customer acceptance
6. **Rejected**: Lost bid, archive
7. **Expired**: Past validity date
8. **Converted**: Became active project

### Revision Management
- Track all changes with timestamps
- Highlight modifications for customer
- Maintain audit trail
- Version comparison tools

## 🎯 Success Metrics

### Quotation Quality
- **Accuracy**: ±3% of final project cost
- **Completeness**: No missing scope items
- **Clarity**: Customer understands fully
- **Compliance**: Passes inspection review

### Business Metrics
- **Win Rate**: 25-40% typical
- **Margin Achievement**: Within 2% of quoted
- **Time to Quote**: <4 hours for standard
- **Customer Satisfaction**: >4.5/5 stars

## 🚨 Risk Factors

### Technical Risks
- Existing conditions differ from plans
- Code interpretation varies by inspector
- Material availability issues
- Skilled labor shortage

### Business Risks
- Price escalation beyond validity
- Scope creep without change orders
- Payment delays affect cash flow
- Competition underpricing

## 🤖 AI Agent Optimization Points

### Where AI Adds Most Value
1. **Load Calculations**: Complex math, code lookups
2. **Material Selection**: Best options for application
3. **Pricing Optimization**: Market intelligence
4. **Compliance Checking**: Automated code review
5. **Document Generation**: Professional formatting

### Human-in-the-Loop Requirements
1. **Final Review**: Experienced estimator check
2. **Special Conditions**: Unique project aspects
3. **Relationship Pricing**: Customer history
4. **Risk Assessment**: Project-specific factors

This context should guide all agent development to ensure accurate, compliant, and competitive electrical quotations.
