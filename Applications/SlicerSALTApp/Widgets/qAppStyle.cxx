/* Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
   file LICENSE.  */

// Qt includes
#include <QDebug>
#include <QLinearGradient>
#include <QMenuBar>
#include <QPainter>
#include <QPalette>
#include <QPushButton>
#if (QT_VERSION < QT_VERSION_CHECK(5, 0, 0))
#include <QCleanlooksStyle>
#else
#include <QStyleFactory>
#endif
#include <QStyleOption>
#include <QToolBar>

// CTK includes
#include <ctkCollapsibleButton.h>

// qMRML includes
#include "qAppStyle.h"

// --------------------------------------------------------------------------
// qSlicerStyle methods

// --------------------------------------------------------------------------
qAppStyle::qAppStyle()
{
#if (QT_VERSION < QT_VERSION_CHECK(5, 0, 0))
  // Slicer uses a QCleanlooksStyle as base style.
  this->setBaseStyle(new QProxyStyle(new QCleanlooksStyle));
#else
  // Slicer uses fusion as base style.
  this->setBaseStyle(new QProxyStyle(QStyleFactory::create("fusion")));
#endif

}

// --------------------------------------------------------------------------
qAppStyle::~qAppStyle()
{
}

//------------------------------------------------------------------------------
QPalette qAppStyle::standardPalette()const
{
  QPalette palette = this->Superclass::standardPalette();

  palette.setColor(QPalette::Active, QPalette::Window, "#eaebee");
  palette.setColor(QPalette::Inactive, QPalette::Window, "#eaebee");
  palette.setColor(QPalette::Disabled, QPalette::Window, "#dedfe1");
  palette.setColor(QPalette::Active, QPalette::WindowText, "#002f4f");
  palette.setColor(QPalette::Inactive, QPalette::WindowText, "#002f4f");
  palette.setColor(QPalette::Disabled, QPalette::WindowText, "#2a404f");
  palette.setColor(QPalette::Active, QPalette::Text, "#002f4f");
  palette.setColor(QPalette::Inactive, QPalette::Text, "#002f4f");
  palette.setColor(QPalette::Disabled, QPalette::Text, "#2a404f");
  palette.setColor(QPalette::Active, QPalette::Base, "#ffffff");
  palette.setColor(QPalette::Inactive, QPalette::Base, "#ffffff");
  palette.setColor(QPalette::Disabled, QPalette::Base, "#eaebee");


  palette.setColor(QPalette::Light, "#ffffff");
  palette.setColor(QPalette::Button, "#dedfe1");
  palette.setColor(QPalette::Mid, "#005f9e");
  palette.setColor(QPalette::Dark, "#005f9e");
  palette.setColor(QPalette::Active, QPalette::ButtonText, "#005f9e");
  palette.setColor(QPalette::Inactive, QPalette::ButtonText, "#005f9e");
  palette.setColor(QPalette::Disabled, QPalette::ButtonText, "#003050");
  palette.setColor(QPalette::Shadow, "#002f4f");

  palette.setColor(QPalette::Highlight, "#009d49");
  palette.setColor(QPalette::HighlightedText, "#ffffff");

  return palette;
}

//------------------------------------------------------------------------------
void qAppStyle::drawComplexControl(ComplexControl control,
                                   const QStyleOptionComplex* option,
                                   QPainter* painter,
                                   const QWidget* widget )const
{
  const_cast<QStyleOptionComplex*>(option)->palette =
    this->tweakWidgetPalette(option->palette, widget);
  this->Superclass::drawComplexControl(control, option, painter, widget);
}

//------------------------------------------------------------------------------
void qAppStyle::drawControl(ControlElement element,
                            const QStyleOption* option,
                            QPainter* painter,
                            const QWidget* widget )const
{
  const_cast<QStyleOption*>(option)->palette =
    this->tweakWidgetPalette(option->palette, widget);

  // For some reason the toolbar paint routine is not respecting the palette.
  // here we make sure the background is correctly drawn.
  if (element == QStyle::CE_ToolBar &&
      qobject_cast<const QToolBar*>(widget))
    {
    painter->fillRect(option->rect, option->palette.brush(QPalette::Window));
    }
  this->Superclass::drawControl(element, option, painter, widget);
}

//------------------------------------------------------------------------------
void qAppStyle::drawPrimitive(PrimitiveElement element,
                              const QStyleOption* option,
                              QPainter* painter,
                              const QWidget* widget )const
{
  const_cast<QStyleOption*>(option)->palette =
    this->tweakWidgetPalette(option->palette, widget);
  this->Superclass::drawPrimitive(element, option, painter, widget);
}

//------------------------------------------------------------------------------
QPalette qAppStyle::tweakWidgetPalette(QPalette widgetPalette,
                                       const QWidget* widget)const
{
  if (!widget)
    {
    return widgetPalette;
    }
  const QPushButton* pushButton =
    qobject_cast<const QPushButton*>(widget);
  if (pushButton &&
      !pushButton->text().isEmpty())
    {
    QColor buttonColor = this->standardPalette().color(QPalette::Dark);
    widgetPalette.setColor(QPalette::Active, QPalette::Button, buttonColor);
    widgetPalette.setColor(QPalette::Inactive, QPalette::Button, buttonColor);
    QColor disabledButtonColor = buttonColor.toHsv();
    disabledButtonColor.setHsvF(disabledButtonColor.hueF(),
                                disabledButtonColor.saturationF() * 0.8,
                                disabledButtonColor.valueF() * 0.9);
    widgetPalette.setColor(QPalette::Disabled, QPalette::Button, disabledButtonColor);
    QColor buttonTextColor =
      this->standardPalette().color(QPalette::Light);
    widgetPalette.setColor(QPalette::Active, QPalette::ButtonText, buttonTextColor);
    widgetPalette.setColor(QPalette::Inactive, QPalette::ButtonText, buttonTextColor);
    QColor disabledButtonTextColor = buttonTextColor.toHsv();
    disabledButtonTextColor.setHsvF(buttonColor.hueF(),
                                    disabledButtonTextColor.saturationF() * 0.3,
                                    disabledButtonTextColor.valueF() * 0.8);
    widgetPalette.setColor(QPalette::Disabled, QPalette::ButtonText, disabledButtonColor);
    }
  if (qobject_cast<const QMenuBar*>(widget))
    {
    QColor highlightColor = this->standardPalette().color(QPalette::Dark);
    //QBrush highlightBrush = this->standardPalette().brush(QPalette::Dark);
    QColor highlightTextColor =
      this->standardPalette().color(QPalette::Light);
    QBrush highlightTextBrush =
      this->standardPalette().brush(QPalette::Light);
    QColor darkColor = this->standardPalette().color(QPalette::Highlight);
    QColor lightColor =
      this->standardPalette().color(QPalette::HighlightedText);

    QLinearGradient hilightGradient(0., 0., 0., 1.);
    hilightGradient.setCoordinateMode(QGradient::ObjectBoundingMode);
    hilightGradient.setColorAt(0., highlightColor);
    hilightGradient.setColorAt(1., highlightColor.darker(120));
    QBrush highlightBrush(hilightGradient);

    widgetPalette.setColor(QPalette::Highlight, darkColor);
    widgetPalette.setColor(QPalette::HighlightedText, lightColor);

    widgetPalette.setColor(QPalette::Window, highlightColor);
    widgetPalette.setColor(QPalette::WindowText, highlightTextColor);
    widgetPalette.setColor(QPalette::Base, highlightColor);
    widgetPalette.setColor(QPalette::Text, highlightTextColor);
    widgetPalette.setColor(QPalette::Button, highlightColor);
    widgetPalette.setColor(QPalette::ButtonText, highlightTextColor);

    widgetPalette.setBrush(QPalette::Window, highlightBrush);
    widgetPalette.setBrush(QPalette::WindowText, highlightTextBrush);
    widgetPalette.setBrush(QPalette::Base, highlightBrush);
    widgetPalette.setBrush(QPalette::Text, highlightTextBrush);
    widgetPalette.setBrush(QPalette::Button, highlightBrush);
    widgetPalette.setBrush(QPalette::ButtonText, highlightTextBrush);
    }
/*
  QWidget* parentWidget = widget->parentWidget();
  QWidget* grandParentWidget = parentWidget? parentWidget->parentWidget() : 0;
  if (qobject_cast<const QToolBar*>(widget) ||
      qobject_cast<QToolBar*>(parentWidget) ||
      qobject_cast<QToolBar*>(grandParentWidget))
    {
    QColor windowColor = this->standardPalette().color(QPalette::Window);

    //QColor highlightColor = this->standardPalette().color(QPalette::Highlight);
    //QColor highlightTextColor =
    //  this->standardPalette().color(QPalette::HighlightedText);
    //QColor darkColor = this->standardPalette().color(QPalette::Dark);
    //QColor lightColor =
    //  this->standardPalette().color(QPalette::Light);
    QColor highlightColor = this->standardPalette().color(QPalette::Dark);
    //QBrush highlightBrush = this->standardPalette().brush(QPalette::Dark);
    QBrush highlightTextBrush =
      this->standardPalette().brush(QPalette::Light);
    QColor darkColor = this->standardPalette().color(QPalette::Highlight);
    QColor lightColor =
      this->standardPalette().color(QPalette::HighlightedText);

    QLinearGradient hilightGradient(0., 0., 0., 1.);
    hilightGradient.setCoordinateMode(QGradient::ObjectBoundingMode);

    hilightGradient.setColorAt(0., highlightColor);
    hilightGradient.setColorAt(1., highlightColor.darker(140));
    QBrush highlightBrush(hilightGradient);

    widgetPalette.setColor(QPalette::Highlight, darkColor);
    widgetPalette.setColor(QPalette::HighlightedText, lightColor);
    widgetPalette.setBrush(QPalette::Window, highlightBrush);
    widgetPalette.setBrush(QPalette::WindowText, highlightTextBrush);
    widgetPalette.setBrush(QPalette::Base, highlightBrush);
    widgetPalette.setBrush(QPalette::Text, highlightTextBrush);
    widgetPalette.setBrush(QPalette::Button, highlightBrush);
    widgetPalette.setBrush(QPalette::ButtonText, highlightTextBrush);
    }
*/
  return widgetPalette;
}

//------------------------------------------------------------------------------
void qAppStyle::polish(QWidget* widget)
{
  this->Superclass::polish(widget);
  ctkCollapsibleButton* collapsibleButton =
    qobject_cast<ctkCollapsibleButton*>(widget);
  if (collapsibleButton)
    {
    collapsibleButton->setFlat(true);
    collapsibleButton->setContentsFrameShadow(QFrame::Sunken);
    }
}
