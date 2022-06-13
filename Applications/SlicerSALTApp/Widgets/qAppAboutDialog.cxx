/*==============================================================================

  Program: 3D Slicer

  Copyright (c) Kitware Inc.

  See COPYRIGHT.txt
  or http://www.slicer.org/copyright/copyright.txt for details.

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  This file was originally developed by Julien Finet, Kitware Inc.
  and was partially funded by NIH grant 3P41RR013218-12S1

==============================================================================*/

// Qt includes

// SlicerApp includes
#include "qAppAboutDialog.h"
#include "qSlicerApplication.h"
#include "ui_qAppAboutDialog.h"

//-----------------------------------------------------------------------------
class qAppAboutDialogPrivate: public Ui_qAppAboutDialog
{
public:
};

//-----------------------------------------------------------------------------
// qAppAboutDialogPrivate methods


//-----------------------------------------------------------------------------
// qAppAboutDialog methods
qAppAboutDialog::qAppAboutDialog(QWidget* parentWidget)
 :QDialog(parentWidget)
  , d_ptr(new qAppAboutDialogPrivate)
{
  Q_D(qAppAboutDialog);
  d->setupUi(this);

  qSlicerApplication* slicer = qSlicerApplication::application();
  d->CreditsTextBrowser->setFontPointSize(25);
  d->CreditsTextBrowser->append(slicer->applicationName());
  d->CreditsTextBrowser->setFontPointSize(11);
  d->CreditsTextBrowser->append("");
  if (!slicer->isCustomMainApplication())
    {
    d->CreditsTextBrowser->append(slicer->applicationVersion() + " " + "r" + slicer->revision()
      + " / " + slicer->repositoryRevision());
    d->CreditsTextBrowser->append("");
    d->CreditsTextBrowser->append("");
    d->CreditsTextBrowser->insertHtml("<a href=\"http://download.slicer.org/\">Download</a> a newer version<br />");
    d->CreditsTextBrowser->append("");
    }
  else
    {
    d->CreditsTextBrowser->append(slicer->applicationVersion() + " (" + slicer->mainApplicationRepositoryRevision() + ")");
    d->CreditsTextBrowser->append("");
    }
  d->CreditsTextBrowser->insertHtml(this->acknowledgment());
  d->CreditsTextBrowser->insertHtml(slicer->libraries());
  d->SlicerLinksTextBrowser->insertHtml(this->copyrights());
  d->CreditsTextBrowser->moveCursor(QTextCursor::Start, QTextCursor::MoveAnchor);

  connect(d->ButtonBox, SIGNAL(rejected()), this, SLOT(close()));
}

//-----------------------------------------------------------------------------
void qAppAboutDialog::setLogo(const QPixmap& newLogo)
{
  Q_D(qAppAboutDialog);
  d->SlicerLabel->setPixmap(newLogo);
}

//-----------------------------------------------------------------------------
qAppAboutDialog::~qAppAboutDialog() = default;

//-----------------------------------------------------------------------------
QString qAppAboutDialog::acknowledgment()const
{
  QString acknowledgmentText(
    "Supported by: NIH and the Slicer Community.<br /><br />"
    "This work is part of the  National Institute of Health grant titled "
    "<i>Shape Analysis Toolbox: From medical images to quantitative insights of anatomy</i>.<br /><br />"
    "SlicerSALT is a  software package for medical image segmentation's "
    "shape analysis. <br /><br />"

    "The SlicerSALT developers gratefully acknowledge funding for this project "
    "NIH NIBIB R01EB021391 as well as the Slicer community. <br /><br />"

    "Ongoing development, maintenance, distribution, and training is managed by "
    "Kitware Inc., University of North Carolina, Chapel Hill, and NYU Tandon School"
    "of Engineering. <br /><br />");
  return acknowledgmentText;
}

//-----------------------------------------------------------------------------
QString qAppAboutDialog::copyrights()const
{
  QString copyrightsText(
    "<table align=\"center\" border=\"0\" width=\"80%\"><tr>"
    "<td align=\"center\"><a href=\"https://github.com/Kitware/SlicerSALT/blob/master/LICENSE\">Licensing Information</a></td>"
    "<td align=\"center\"><a href=\"http://salt.slicer.org/\">Website</a></td>"
    "</tr></table>");
  return copyrightsText;
}