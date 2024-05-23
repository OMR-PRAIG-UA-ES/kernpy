from kernpy.core import Importer, ExportOptions


def read_kern(input_file: str):
    """
    Read a kern file and return a Score object.

    Args:
        inputpath: The path to the kern file.

    Returns:
        score: The score object.

    Examples:
        >>> import kernpy
        >>> score = kernpy.read_kern('path/to/file.krn')
        >>> print(score)
    """
    importer = Importer()
    importer.import_file(input_file)

    if len(importer.errors):
        raise Exception(f'ERROR: {input_file} has errors {importer.getErrorMessages()}')

    # TODO: Store the HumdrumImporter object in the Score object
    score = Score("a")
    return score

class Score:
    def __init__(self, name):
        self.name = name
        ...

    def transpose(self, interval: int):
        """
        Transpose the score by a chromatic interval.
        Keep the same notes semantic interval. Even if double or triple accidentals are used.

        Args:
            interval: The chromatic interval to transpose the score.
            
        Returns:
            new_score: The transposed score.

        Examples:
            >>> import kernpy
            >>> score = kernpy.read_kern('path/to/file.krn')
            >>> # Transpose 2 semitones up
            >>> s1 = score.transpose(2)
            >>> # Transpose 2 semitones down
            >>> s2 = score.transpose(-2)
            >>> # Export it to a file
            >>> s1.to_krn('path/to/up2.krn')
            >>> s2.to_krn('path/to/down2.krn')
        """
        raise NotImplementedError()

    def measure_from_time(self, time: float) -> int:
        """
        Greater number of the measure where the time is not greater than 10 seconds

        Args:
            time: The max time in seconds.

        Returns:
            measure: The measure number.

        Examples:
            >>> import kernpy
            >>> score = kernpy.read_kern('path/to/file.krn')
            >>> # Get the measure at 10 seconds
            >>> measure = score.measure_from_time(10)
            >>> # Greater number of the measure where the time is not greater than 10 seconds
            >>> print(measure)
        """
        raise NotImplementedError()

    def extract_spine(self, spine):
        """
        Extract a spine from the score. TODO:
        """
        raise NotImplementedError()

    def extract_measures(self, from_measure=None, to_measure=None):
        """
        Extract a range of measures from the score and return a new score.

        Args:
            from_measure: The measure to start the extraction. The first measure starts at 0.
            to_measure: The measure to end the extraction. The last measure is included. \
                        The last measure ends at len(score.measures) - 1.
        """
        raise NotImplementedError()

    def tokens(self) -> set:
        """
        Return a set of tokens in the score.

        Returns:
            tokens: A set of tokens in the score.

        Examples:
            >>> import kernpy
            >>> score = kernpy.read_kern('path/to/file.krn')
            >>> tokens = score.tokens()
            >>> print(tokens)
            {"2r", "4G", "8c", "|" }

        """
        raise NotImplementedError()

    def to_krn(self):
        raise NotImplementedError()

    def to_ekrn(self):
        raise NotImplementedError()

    def export(self, options: ExportOptions):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()
