import unittest

from loose_version_comparator import Version, compare


class TestTokenisation(unittest.TestCase):
    def test_dot_separated(self):
        self.assertEqual(Version("1.2.3").tokens, [1, 2, 3])

    def test_mixed_separators_collapse(self):
        self.assertEqual(Version("1-2_3.4").tokens, [1, 2, 3, 4])

    def test_numeric_promotion(self):
        # 10 must beat 9 as integers, not as strings.
        self.assertLess(Version("1.9"), Version("1.10"))

    def test_alpha_token_kept(self):
        self.assertEqual(Version("1.0-alpha").tokens, [1, 0, "alpha"])

    def test_empty_string(self):
        self.assertEqual(Version("").tokens, [])

    def test_leading_and_trailing_separators(self):
        self.assertEqual(Version("..1.2..").tokens, [1, 2])

    def test_mixed_alnum_chunk_stays_string(self):
        # "12a" is not pure digits, so it stays a string token.
        self.assertEqual(Version("12a").tokens, ["12a"])


class TestEquality(unittest.TestCase):
    def test_trailing_zero_noop(self):
        self.assertEqual(Version("1.0"), Version("1.0.0"))

    def test_different_separators_same_tokens(self):
        self.assertEqual(Version("1.2.3"), Version("1-2-3"))

    def test_hash_matches_equality(self):
        self.assertEqual(hash(Version("1.0")), hash(Version("1.0.0")))

    def test_unequal(self):
        self.assertNotEqual(Version("1.0"), Version("1.1"))


class TestOrdering(unittest.TestCase):
    def test_numeric_release_beats_prerelease(self):
        self.assertGreater(Version("1.0.0"), Version("1.0.0-alpha"))

    def test_prerelease_vs_release_shorter_wins(self):
        # 1.0 is a release; 1.0-alpha is a prerelease. Release wins.
        self.assertGreater(Version("1.0"), Version("1.0-alpha"))

    def test_two_prereleases_ordinal(self):
        # No keyword ladder: plain string compare. 'alpha' < 'beta'.
        self.assertLess(Version("1.0-alpha"), Version("1.0-beta"))

    def test_prerelease_does_not_beat_release_by_keyword(self):
        # 'rc' would beat 'beta' under a semver ladder, but we do not do that.
        # Under ordinal compare 'beta' < 'rc', which is what we assert.
        self.assertLess(Version("1.0-beta"), Version("1.0-rc"))

    def test_extra_positive_int_makes_greater(self):
        self.assertGreater(Version("1.0.1"), Version("1.0"))

    def test_extra_zero_is_noop(self):
        self.assertEqual(Version("1.0.0"), Version("1.0"))

    def test_extra_prerelease_makes_lesser(self):
        self.assertLess(Version("1.0-alpha"), Version("1.0"))

    def test_compare_helper_minus_one(self):
        self.assertEqual(compare("1.0", "2.0"), -1)

    def test_compare_helper_zero(self):
        self.assertEqual(compare("2.0", "2.0"), 0)

    def test_compare_helper_plus_one(self):
        self.assertEqual(compare("2.0", "1.0"), 1)

    def test_total_ordering_chain(self):
        versions = [Version(v) for v in ("1.10.0", "1.9.0", "1.0.0", "1.0.0-alpha")]
        ordered = sorted(versions)
        self.assertEqual([str(v.raw) for v in ordered],
                         ["1.0.0-alpha", "1.0.0", "1.9.0", "1.10.0"])


class TestTypeErrors(unittest.TestCase):
    def test_non_string_rejected(self):
        with self.assertRaises(TypeError):
            Version(123)  # type: ignore[arg-type]

    def test_compare_with_non_version_returns_notimplemented(self):
        # Equality against an unrelated type must not raise; it returns False.
        self.assertFalse(Version("1.0") == "1.0")


if __name__ == "__main__":
    unittest.main()
