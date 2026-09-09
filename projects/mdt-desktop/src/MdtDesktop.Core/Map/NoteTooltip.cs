namespace MdtDesktop.Core.Map;

/// <summary>
/// What a note pin's tooltip says, as content rather than as a control.
/// </summary>
/// <remarks>
/// The same seam <see cref="MobTooltip"/> establishes, and deliberately a separate type rather
/// than a widening of it: a note has no role, no forces and no pull, so every field of a mob
/// tooltip would be empty. Two small content types plus two <c>DataTemplate</c>s cost less than
/// one type that means different things depending on which half is filled in.
/// </remarks>
public sealed record NoteTooltip
{
    /// <summary>The pin's number and the note's first line — its heading, where there is one.</summary>
    public required string Heading { get; init; }

    /// <summary>Everything after the first line. Empty for a one-line note.</summary>
    public required string Body { get; init; }

    /// <summary>False when there is nothing but a heading, so the template can omit the row.</summary>
    public bool HasBody => Body.Length > 0;

    /// <summary>
    /// Builds the tooltip for one note.
    /// </summary>
    /// <remarks>
    /// ⚠ A note's text can legitimately be empty — MDT's toolbar creates a note with
    /// <c>d[5] = ""</c> and fills it in afterwards, so an abandoned note is a real wire shape
    /// and MDT still draws its pin. The fallback wording is decided here, where it is testable,
    /// rather than in a draw loop where an empty tooltip box would simply appear.
    /// </remarks>
    public static NoteTooltip Build(AnnotationOverlay note)
        => new()
        {
            Heading = note.Title.Length > 0 ? $"{note.Number}. {note.Title}" : $"{note.Number}. (empty note)",
            Body = note.Body,
        };
}
