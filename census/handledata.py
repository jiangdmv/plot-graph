import math
import scipy.stats as stat
import plotly.graph_objects as go


def computeCount(firstDigits):
    n = len(firstDigits)

    observed = [0] * 9
    for digit in firstDigits:
        observed[digit - 1] += 1

    expected = [0] * 9
    for i in range(9):
        expected[i] = math.log10(1 + 1 / (i + 1)) * n

    return [observed, expected]


def plotCount(observed, expected):
    idx = [i for i in range(1, 10)]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=idx, y=observed, name="Observed"))
    fig.add_trace(go.Bar(x=idx, y=expected, name="Expected"))
    fig.update_layout(title_text="Frequency of Observed and Benford's Law Predicted First Digits",
                      autosize=False, width=800, height=500, bargap=0, bargroupgap=0)
    fig.update_xaxes(tickvals=idx)

    return fig.to_html()


def chisq_stat(o, e):
    return sum([(o - e) ** 2 / e for (o, e) in zip(o, e)])


def conclude(observed, expected, alpha):
    statistic = chisq_stat(observed, expected)
    pvalue = 1 - stat.chi2.cdf(statistic, 8)
    if pvalue > alpha:
        significant = "not "
    else:
        significant = ""

    conclusion = "Observed distribution is {0}significantly different from Benford's law based on a Chi-squared test " \
                 "with 8 degrees of freedom and alpha={1}. \nTest statistics={2}. P-value={3}".format(significant,
                                                                                                      alpha,
                                                                                                      round(statistic,
                                                                                                            3),
                                                                                                      round(pvalue, 5))

    return conclusion
