from __future__ import annotations

import argparse
from datetime import date
from typing import Dict, List, Optional, Sequence, Set


class Person:
    def __init__(self, first_name: str, last_name: str, national_id: str) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.national_id = national_id

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_national_id(self) -> str:
        return self.national_id


class User:
    def __init__(self, user_id: Optional[int], email: str, password_hash: str, role: str, created_at: str) -> None:
        self.id = user_id
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at

    def authenticate(self, password: str) -> bool:
        return self.password_hash == password


class Admin(User):
    def __init__(self, user_id: Optional[int], email: str, password_hash: str, created_at: str) -> None:
        super().__init__(user_id, email, password_hash, "admin", created_at)

    def manage_election(self, election: "Election") -> str:
        return f"Admin is managing: {election.title}"


class Candidate(Person):
    def __init__(self, candidate_id: Optional[int], first_name: str, last_name: str, national_id: str, election_id: int, profile: str) -> None:
        super().__init__(first_name, last_name, national_id)
        self.id = candidate_id
        self.election_id = election_id
        self.profile = profile

    def get_id(self) -> Optional[int]:
        return self.id

    def get_election_id(self) -> int:
        return self.election_id

    def get_profile(self) -> str:
        return self.profile


class Voter(User):
    def __init__(self, user_id: Optional[int], email: str, password_hash: str, role: str, created_at: str, person: Person, verified: bool) -> None:
        super().__init__(user_id, email, password_hash, role, created_at)
        self.person = person
        self.verified = verified
        self._voted_elections: Set[int] = set()

    def get_profile(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "email": self.email,
            "name": self.person.get_full_name(),
            "national_id": self.person.get_national_id(),
            "role": self.role,
            "verified": self.verified,
        }

    def is_verified(self) -> bool:
        return self.verified

    def cast_vote(self, election: "Election", candidate: Candidate) -> bool:
        if not self.is_verified():
            return False
        if election.id is None or election.id in self._voted_elections:
            return False
        if not election.can_accept_votes():
            return False
        election.add_vote(candidate)
        self._voted_elections.add(election.id)
        return True


class Election:
    def __init__(self, election_id: Optional[int], title: str, description: str, start_date: str, end_date: str, published: bool, active: bool, created_by: Optional[int]) -> None:
        self.id = election_id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.published = published
        self.active = active
        self.created_by = created_by
        self._results: Dict[int, int] = {}
        self._candidates: List[Candidate] = []

    def add_candidate(self, candidate: Candidate) -> None:
        self._candidates.append(candidate)

    def get_candidates(self) -> List[Candidate]:
        return list(self._candidates)

    def add_vote(self, candidate: Candidate) -> None:
        candidate_id = candidate.get_id()
        if candidate_id is None:
            raise ValueError("Candidate must have an id before voting")
        self._results[candidate_id] = self._results.get(candidate_id, 0) + 1

    def get_results(self) -> Dict[int, int]:
        return dict(self._results)

    def is_active(self) -> bool:
        today = date.today()
        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)
        return self.active and start <= today <= end

    def can_accept_votes(self) -> bool:
        return self.is_published() and self.is_active()

    def is_published(self) -> bool:
        return self.published

    def get_status(self) -> str:
        if not self.active:
            return "Closed"
        today = date.today()
        start = date.fromisoformat(self.start_date)
        end = date.fromisoformat(self.end_date)
        if today < start:
            return "Scheduled"
        if today > end:
            return "Closed"
        return "Open"


class VotingSystem:
    def __init__(self) -> None:
        self.admins: List[Admin] = []
        self.elections: List[Election] = []
        self.candidates: List[Candidate] = []
        self.voters: List[Voter] = []
        self._next_election_id = 1
        self._next_candidate_id = 1
        self._next_voter_id = 1

    def create_election(self, title: str, description: str, start_date: str, end_date: str, published: bool = True, active: bool = True, created_by: Optional[int] = None) -> Election:
        election = Election(self._next_election_id, title, description, start_date, end_date, published, active, created_by)
        self.elections.append(election)
        self._next_election_id += 1
        return election

    def add_candidate(self, first_name: str, last_name: str, national_id: str, election_id: int, profile: str) -> Candidate:
        election = self.get_election(election_id)
        if election is None:
            raise ValueError(f"Election {election_id} does not exist")

        candidate = Candidate(self._next_candidate_id, first_name, last_name, national_id, election_id, profile)
        self.candidates.append(candidate)
        election.add_candidate(candidate)
        self._next_candidate_id += 1
        return candidate

    def register_voter(self, first_name: str, last_name: str, national_id: str, email: str, password_hash: str, verified: bool = True) -> Voter:
        person = Person(first_name, last_name, national_id)
        voter = Voter(self._next_voter_id, email, password_hash, "voter", date.today().isoformat(), person, verified)
        self.voters.append(voter)
        self._next_voter_id += 1
        return voter

    def get_election(self, election_id: int) -> Optional[Election]:
        for election in self.elections:
            if election.id == election_id:
                return election
        return None

    def get_voter(self, voter_id: int) -> Optional[Voter]:
        for voter in self.voters:
            if voter.id == voter_id:
                return voter
        return None

    def vote(self, voter: Voter, election: Election, candidate: Candidate) -> bool:
        return voter.cast_vote(election, candidate)

    def list_elections(self) -> List[Election]:
        return list(self.elections)

    def list_candidates(self, election_id: int) -> List[Candidate]:
        election = self.get_election(election_id)
        if election is None:
            return []
        return election.get_candidates()

    def get_results(self, election_id: int) -> Dict[int, int]:
        election = self.get_election(election_id)
        if election is None:
            return {}
        return election.get_results()


class VotingCLI:
    def __init__(self, system: Optional[VotingSystem] = None) -> None:
        self.system = system or VotingSystem()

    def _show_menu(self) -> None:
        print("\nVoting System Menu")
        print("1. Create election")
        print("2. Add candidate")
        print("3. Register voter")
        print("4. Vote")
        print("5. List elections")
        print("6. Show results")
        print("0. Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            title = input("Election title: ")
            description = input("Description: ")
            start_date = input("Start date (YYYY-MM-DD): ")
            end_date = input("End date (YYYY-MM-DD): ")
            election = self.system.create_election(title, description, start_date, end_date)
            print(f"Election created: {election.id} - {election.title}")
        elif choice == "2":
            election_id = int(input("Election ID: "))
            first_name = input("Candidate first name: ")
            last_name = input("Candidate last name: ")
            national_id = input("National ID: ")
            profile = input("Profile: ")
            candidate = self.system.add_candidate(first_name, last_name, national_id, election_id, profile)
            print(f"Candidate added: {candidate.id} - {candidate.get_full_name()}")
        elif choice == "3":
            first_name = input("Voter first name: ")
            last_name = input("Voter last name: ")
            national_id = input("National ID: ")
            email = input("Email: ")
            password = input("Password: ")
            voter = self.system.register_voter(first_name, last_name, national_id, email, password)
            print(f"Voter registered: {voter.id} - {voter.get_profile()['name']}")
        elif choice == "4":
            voter_id = int(input("Voter ID: "))
            election_id = int(input("Election ID: "))
            candidate_id = int(input("Candidate ID: "))
            voter = self.system.get_voter(voter_id)
            election = self.system.get_election(election_id)
            candidate = None
            for item in self.system.candidates:
                if item.id == candidate_id:
                    candidate = item
                    break
            if voter is None or election is None or candidate is None:
                print("Invalid voter, election, or candidate")
            else:
                success = self.system.vote(voter, election, candidate)
                print("Vote accepted" if success else "Vote rejected")
        elif choice == "5":
            for election in self.system.list_elections():
                print(f"{election.id}: {election.title}")
        elif choice == "6":
            election_id = int(input("Election ID: "))
            for candidate_id, count in self.system.get_results(election_id).items():
                print(f"Candidate {candidate_id}: {count}")
        elif choice == "0":
            print("Goodbye!")
        else:
            print("Invalid choice")

    def run(self, argv: Optional[Sequence[str]] = None) -> int:
        if argv is None or len(argv) == 0:
            self._show_menu()
            return 0

        parser = argparse.ArgumentParser(description="Simple OOP-based voting CLI")
        subparsers = parser.add_subparsers(dest="command")

        create_election = subparsers.add_parser("create-election", help="Create a new election")
        create_election.add_argument("title")
        create_election.add_argument("description")
        create_election.add_argument("start_date")
        create_election.add_argument("end_date")

        add_candidate = subparsers.add_parser("add-candidate", help="Add a candidate to an election")
        add_candidate.add_argument("election_id", type=int)
        add_candidate.add_argument("first_name")
        add_candidate.add_argument("last_name")
        add_candidate.add_argument("national_id")
        add_candidate.add_argument("profile")

        register_voter = subparsers.add_parser("register-voter", help="Register a voter")
        register_voter.add_argument("first_name")
        register_voter.add_argument("last_name")
        register_voter.add_argument("national_id")
        register_voter.add_argument("email")
        register_voter.add_argument("password")

        vote = subparsers.add_parser("vote", help="Cast a vote")
        vote.add_argument("voter_id", type=int)
        vote.add_argument("election_id", type=int)
        vote.add_argument("candidate_id", type=int)

        list_elections = subparsers.add_parser("list-elections", help="List all elections")
        list_elections.add_argument("--verbose", action="store_true")

        show_results = subparsers.add_parser("show-results", help="Show results for an election")
        show_results.add_argument("election_id", type=int)

        args = parser.parse_args(argv)

        if not args.command:
            self._show_menu()
            return 0

        if args.command == "create-election":
            election = self.system.create_election(args.title, args.description, args.start_date, args.end_date)
            print(f"Election created: {election.id} - {election.title}")
        elif args.command == "add-candidate":
            candidate = self.system.add_candidate(args.first_name, args.last_name, args.national_id, args.election_id, args.profile)
            print(f"Candidate added: {candidate.id} - {candidate.get_full_name()}")
        elif args.command == "register-voter":
            voter = self.system.register_voter(args.first_name, args.last_name, args.national_id, args.email, args.password)
            print(f"Voter registered: {voter.id} - {voter.get_profile()['name']}")
        elif args.command == "vote":
            voter = self.system.get_voter(args.voter_id)
            election = self.system.get_election(args.election_id)
            candidate = None
            for item in self.system.candidates:
                if item.id == args.candidate_id:
                    candidate = item
                    break
            if voter is None or election is None or candidate is None:
                print("Invalid voter, election, or candidate")
                return 1
            success = self.system.vote(voter, election, candidate)
            print("Vote accepted" if success else "Vote rejected")
        elif args.command == "list-elections":
            for election in self.system.list_elections():
                if args.verbose:
                    print(f"{election.id}: {election.title} [{election.get_status()}]")
                else:
                    print(f"{election.id}: {election.title}")
        elif args.command == "show-results":
            for candidate_id, count in self.system.get_results(args.election_id).items():
                print(f"Candidate {candidate_id}: {count}")
        return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    cli = VotingCLI()
    return cli.run(argv)


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["Admin", "Candidate", "Election", "Person", "User", "Voter", "VotingCLI", "VotingSystem"]
