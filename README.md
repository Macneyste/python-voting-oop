# Python Voting System (OOP)

A professional, object-oriented voting system built with Python that demonstrates solid OOP principles with a complete CLI interface for managing elections, candidates, and voters.

## 📋 Features

- **Election Management**: Create and manage multiple elections with customizable dates
- **Candidate Registration**: Add candidates to elections with profiles
- **Voter Registration**: Register and verify voters with secure authentication
- **Vote Casting**: Cast votes with built-in validation and duplicate prevention
- **Results Tracking**: View election results in real-time
- **Status Tracking**: Automatic election status management (Scheduled, Open, Closed)
- **CLI Interface**: Both interactive menu and command-line argument support

## 🏗️ Architecture

### Class Hierarchy

```
Person
├── Candidate

User
├── Admin
└── Voter

Election
VotingSystem
VotingCLI
```

### Core Classes

- **`Person`**: Base class for individuals (first name, last name, national ID)
- **`User`**: Authentication base class with role-based access control
- **`Admin`**: User with election management privileges
- **`Voter`**: User who can cast votes with verification tracking
- **`Candidate`**: Person registered for an election with profile information
- **`Election`**: Manages voting period, candidates, and vote tallying
- **`VotingSystem`**: Core business logic and data management
- **`VotingCLI`**: Command-line interface for user interactions

## 🚀 Installation

### Requirements
- Python 3.7+

### Setup
```bash
# Clone the repository
git clone https://github.com/Macneyste/python-voting-oop.git
cd python-voting-oop

# No external dependencies required - uses only Python standard library
```

## 💻 Usage

### Interactive Menu Mode

```bash
python voting_system.py
```

This launches an interactive menu with the following options:
1. Create election
2. Add candidate
3. Register voter
4. Cast vote
5. List elections
6. Show results

### Command-Line Mode

#### Create an Election
```bash
python voting_system.py create-election "Presidential Election 2024" "General election" 2024-01-01 2024-01-31
```

#### Register a Voter
```bash
python voting_system.py register-voter John Doe ABC123456 john@example.com securepass123
```

#### Add a Candidate
```bash
python voting_system.py add-candidate 1 Jane Smith XYZ789012 "Presidential candidate with 20 years experience"
```

#### Cast a Vote
```bash
python voting_system.py vote 1 1 1
# Format: vote <voter_id> <election_id> <candidate_id>
```

#### List Elections
```bash
python voting_system.py list-elections
python voting_system.py list-elections --verbose  # Shows election status
```

#### Show Results
```bash
python voting_system.py show-results 1
# Shows vote count for each candidate in election 1
```

## 📊 Election Status

Elections automatically track their status based on current date:

- **Scheduled**: Election date has not started
- **Open**: Election is currently accepting votes
- **Closed**: Election date has passed or marked as inactive

## 🔐 Security Features

- Role-based access control (Admin, Voter)
- User verification status tracking
- Duplicate vote prevention per voter per election
- Password hashing support (comparison-based authentication)
- National ID validation for voter identity

## 📝 Example Workflow

```python
from voting_system import VotingSystem

# Initialize system
system = VotingSystem()

# Create election
election = system.create_election(
    "City Council Election",
    "Annual city council election",
    "2024-06-01",
    "2024-06-30"
)

# Register candidates
candidate1 = system.add_candidate("Alice", "Johnson", "ID001", election.id, "Education advocate")
candidate2 = system.add_candidate("Bob", "Smith", "ID002", election.id, "Infrastructure expert")

# Register voter
voter = system.register_voter("Charlie", "Brown", "ID003", "charlie@example.com", "password123")

# Cast vote
system.vote(voter, election, candidate1)

# Get results
results = system.get_results(election.id)
print(results)  # {1: 1}  - Candidate 1 has 1 vote
```

## 🛠️ Class Methods Reference

### VotingSystem

| Method | Description |
|--------|-------------|
| `create_election()` | Create a new election |
| `add_candidate()` | Register a candidate for an election |
| `register_voter()` | Register a new voter |
| `vote()` | Cast a vote from a voter to a candidate |
| `get_election()` | Retrieve an election by ID |
| `get_voter()` | Retrieve a voter by ID |
| `list_elections()` | Get all elections |
| `list_candidates()` | Get all candidates for an election |
| `get_results()` | Get vote counts for an election |

### Voter

| Method | Description |
|--------|-------------|
| `cast_vote()` | Cast a vote (validates voter and election status) |
| `get_profile()` | Get voter profile information |
| `is_verified()` | Check verification status |

### Election

| Method | Description |
|--------|-------------|
| `add_candidate()` | Add a candidate to the election |
| `add_vote()` | Record a vote |
| `get_candidates()` | Get all candidates |
| `get_results()` | Get vote tallies |
| `is_active()` | Check if election is currently active |
| `can_accept_votes()` | Check if voting is permitted |
| `get_status()` | Get current election status |

## 📚 Type Hints

The entire codebase uses Python type hints for better code clarity and IDE support:

```python
def register_voter(
    self, 
    first_name: str, 
    last_name: str, 
    national_id: str, 
    email: str, 
    password_hash: str, 
    verified: bool = True
) -> Voter:
```

## ✅ Validation & Error Handling

- Duplicate vote prevention per voter per election
- Election date validation
- Voter verification requirement for voting
- National ID format support
- Graceful error messages for invalid operations

## 🧪 Testing

The system includes comprehensive validation:

```python
# Example: Voting validation
- Voter must be verified
- Election must be published
- Election must be within date range
- Voter cannot vote twice in same election
- Candidate must belong to the election
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Submit issues for bugs or feature requests
- Create pull requests with improvements
- Improve documentation and examples

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Macneyste** - [GitHub Profile](https://github.com/Macneyste)

## 📞 Support

For questions or issues:
- Open an issue on [GitHub Issues](https://github.com/Macneyste/python-voting-oop/issues)
- Check existing documentation

---

**Last Updated**: July 2024
